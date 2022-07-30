from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
from store.models import Product
import datetime
import json

# Create your views here.
def place_order(request):
  user          = request.user

  cart_items    = CartItem.objects.filter(user=user)
  if not cart_items.exists():
    return redirect('home')
  
  sub_total   = 0
  tax         = 0
  quantity    = 0
  for cart_item in cart_items:
    sub_total += (cart_item.product.price * cart_item.quantity)
    quantity  += cart_item.quantity

  tax = (sub_total * 18) // 100
  total = sub_total + tax

  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      order                   = Order()
      order.user              = user
      order.first_name        = form.cleaned_data['first_name']
      order.last_name         = form.cleaned_data['last_name']
      order.email             = form.cleaned_data['email']
      order.address_line_1    = form.cleaned_data['address_line_1']
      order.phone_number      = form.cleaned_data['phone_number']
      order.country           = form.cleaned_data['country']
      order.state             = form.cleaned_data['state']
      order.city              = form.cleaned_data['city']
      order.pincode           = form.cleaned_data['pincode']
      order.tax               = tax
      order.order_total       = total
      order.ip                = request.META.get('REMOTE_ADDR')
      order.save()

      date                  = datetime.date.today()
      current_date          = date.strftime('%Y%m%d')
      order_number          = current_date + str(order.id)
      order.order_number    = order_number
      order.save()

      context = {
        'order'       : order,
        'subtotal'    : sub_total,
        'tax'         : tax,
        'cart_items'  : cart_items,
      }
      return render(request, 'orders/payment.html', context)


  return render(request,'orders/invoice.html')


def payment(request):
  data    = json.loads(request.body)
  order   = Order.objects.get(user=request.user,is_ordered=False,order_number=data['orderID'])

  payment = Payment(
    user              = request.user,
    payment_id        = data['transID'],
    payment_method    = data['payment_method'],
    ammount_paid      = order.order_total,
    status            = data['status']
  )
  payment.save()

  order.payment       = payment
  order.is_ordered    = True
  order.save()

  cart_items = CartItem.objects.filter(user=request.user)
  for cart_item in cart_items:
    order_product                 = OrderProduct()
    order_product.order_id        = order.id
    order_product.payment         = payment
    order_product.user_id         = request.user.id
    order_product.product_id      = cart_item.product_id
    order_product.quantity        = cart_item.quantity
    order_product.product_price   = cart_item.product.price
    order_product.ordered         = True
    order_product.save()

    variations  = cart_item.variation.all()
    order_product.variation.set(variations)
    order_product.save()

    product         = Product.objects.get(id=cart_item.product_id)
    product.stock   -= cart_item.quantity
    product.save()

  cart_items.delete()

  return redirect('place_order')


def payment_complete(request):
  order_id = request.GET.get('order_id')
  order = Order.objects.get(order_number=order_id)
  order_products = OrderProduct.objects.filter(order=order)
  context = {
    'order_products': order_products,
    'order': order
  }
  return render(request,'orders/invoice.html',context)
