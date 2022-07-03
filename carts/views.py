from django.shortcuts import render,redirect , get_object_or_404
from store.models import Product
from .models import Cart,CartItem ,WishList

# Create your views here.
def _cart_id(request):
  cart = request.session.session_key
  if cart is None:
    cart = request.session.create()
  return cart


def remove_cart(request,product_id):
  product   = get_object_or_404(Product,id=product_id)
  cart      = get_object_or_404(Cart,cart_id = _cart_id(request))
  cart_item = get_object_or_404(CartItem,product=product,cart=cart)
  cart_item.delete() 
  return redirect('cart')


def minus_cart(request,product_id):
  product   = get_object_or_404(Product,id=product_id)
  cart      = get_object_or_404(Cart,cart_id = _cart_id(request))
  cart_item = get_object_or_404(CartItem,product=product,cart=cart)

  if cart_item.quantity > 1:
    cart_item.quantity -= 1 
    cart_item.save()
  else:
    return redirect('remove_cart')

  return redirect('cart')

def add_cart(request,product_id):
  product = Product.objects.get(id=product_id)
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except:
    cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

  try:
    wishlist = WishList.objects.get(product=product,cart=cart)
    wishlist.delete()
  except:
    pass

  try:
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.quantity += 1
    cart_item.save()
  except:
    cart_item = CartItem.objects.create(
      product   = product,
      cart      = cart,
      quantity  = 1
    )
    cart_item.save()
  
  return redirect('cart')


def cart(request):
  try:
    cart = Cart.objects.get(cart_id = _cart_id(request))
  except:
    cart = None
  # print('cart :=>',cart)
  if cart is not None:
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal = 0 
    for cart_item in cart_items:
      subtotal += (cart_item.quantity * cart_item.product.price)
    tax = (subtotal * 18) // 100

    context = {
      'cart_items'    : cart_items,
      'empty'         : not cart_items.exists(),
      'subtotal'      : subtotal,
      'tax'           : tax
    }
  else:
    context = {
      'empty':True
    }
  return render(request,'cart.html',context)


def add_wishlist(request,product_id):
  product = get_object_or_404(Product,id=product_id)
  cart    = get_object_or_404(Cart,cart_id=_cart_id(request))

  try:
    cart_item = CartItem.objects.get(cart=cart,product=product)
    cart_item.delete() 
  except:
    pass

  try:
    wishlist = WishList.objects.get(cart=cart, product=product)
  except:
    wishlist = WishList.objects.create(product=product,cart=cart)

  return redirect('cart')

def show_wishlist(request):
  cart = Cart.objects.get(cart_id = _cart_id(request))
  wishlist = WishList.objects.filter(cart=cart)
  context = {
    'wishlist': wishlist,
    'empty'   : not wishlist.exists(),
    }
  return render(request, 'wishlist.html', context)


def remove_wishlist(request,product_id):
  product = get_object_or_404(Product,id=product_id)
  cart = get_object_or_404(Cart,cart_id=_cart_id(request))
  wishlist = get_object_or_404(WishList,product=product,cart=cart)
  wishlist.delete()
  return redirect('show_wishlist')
