from django.shortcuts import render,redirect , get_object_or_404
from store.models import Product,Variation
from .models import Cart,CartItem ,WishList
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
  cart = request.session.session_key
  if cart is None:
    cart = request.session.create()
  return cart


def remove_cart(request,product_id,cart_item_id):
  product   = get_object_or_404(Product,id=product_id)
  cart      = get_object_or_404(Cart,cart_id = _cart_id(request))
  if request.user.is_authenticated:
    cart_item = get_object_or_404(CartItem,product=product,user=request.user,id=cart_item_id)
  else:
    cart_item = get_object_or_404(CartItem,product=product,cart=cart,id=cart_item_id)
  cart_item.delete() 
  return redirect('cart')


def minus_cart(request,product_id,cart_item_id):
  product   = get_object_or_404(Product,id=product_id)
  cart      = get_object_or_404(Cart,cart_id = _cart_id(request))
  
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
      cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    if cart_item.quantity > 1:
      cart_item.quantity -= 1 
      cart_item.save()
    else:
      return redirect(reverse('remove_cart',args=[product_id,cart_item_id]))
  except:
    pass
  return redirect('cart')

def add_cart(request,product_id):
  product = Product.objects.get(id=product_id)
  variation_list = []
  if request.method == 'POST':
    for key in request.POST:
      value = request.POST[key]
      try:
        variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
        variation_list.append(variation)
      except:
        pass

  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except:
    cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

  if request.user.is_authenticated:
    cart_items = CartItem.objects.filter(product=product,user=request.user)
  else:
    cart_items = CartItem.objects.filter(product=product,cart=cart)

  cart_item_exists = cart_items.exists()
  if cart_item_exists:
    existing_variation_list = []
    ids = []
    for item in cart_items:
      existing_variation_list.append(list(item.variation.all()))
      ids.append(item.id)

    if variation_list in existing_variation_list:
      item_index = existing_variation_list.index(variation_list)
      item_id = ids[item_index]
      cart_item = CartItem.objects.get(id=item_id)
      cart_item.quantity += 1
    else:
      if request.user.is_authenticated:
        cart_item = CartItem.objects.create(product=product,user=request.user,quantity=1)
      else:
        cart_item = CartItem.objects.create(product=product,cart=cart,quantity=1)
      if len(variation_list)>0:
        cart_item.variation.add(*variation_list)
  else:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.create(product=product,user=request.user,quantity=1)
    else:
      cart_item = CartItem.objects.create(product=product,cart=cart,quantity=1)
    cart_item.variation.add(*variation_list)
  cart_item.save()
  
  return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart(request):
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user)
    else:
      cart = Cart.objects.get(cart_id = _cart_id(request))
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
  except:
    context = {
      'empty':True
    }

    
    
  return render(request,'carts/cart.html',context)


def add_wishlist(request,product_id):
  product = get_object_or_404(Product,id=product_id)
  cart    = get_object_or_404(Cart,cart_id=_cart_id(request))

  try:
    wishlist = WishList.objects.get(cart=cart, product=product)
  except:
    wishlist = WishList.objects.create(product=product,cart=cart)
  
  return redirect(request.META.get('HTTP_REFERER', 'home'))

def show_wishlist(request):
  cart = Cart.objects.get(cart_id = _cart_id(request))
  wishlist = WishList.objects.filter(cart=cart)
  context = {
    'wishlist': wishlist,
    'empty'   : not wishlist.exists(),
    }
  
  return render(request, 'carts/wishlist.html', context)


def remove_wishlist(request,product_id):
  product = get_object_or_404(Product,id=product_id)
  cart = get_object_or_404(Cart,cart_id=_cart_id(request))
  wishlist = get_object_or_404(WishList,product=product,cart=cart)
  wishlist.delete()
  return redirect(request.META.get('HTTP_REFERER','show_wishlist'))


def move_to_cart(request,product_id):
  product = Product.objects.get(id=product_id)
  wishlist = WishList.objects.get(product=product)
  wishlist.delete()
  try:
    cart_item = CartItem.objects.get(product=product)
  except:
    return redirect(reverse('add_cart',args=[product_id]))
  return redirect('show_wishlist')

def move_to_wishlist(request, cart_item_id):
  cart_item = CartItem.objects.get(id=cart_item_id)
  product = Product.objects.get(id=cart_item.product_id)
  cart_item.delete()
  try:
    wishlist = WishList.objects.get(product=product)
  except:
    return redirect(reverse('wishlist',args=[product.id]))

  return redirect('cart')

@login_required(login_url='login')
def checkout(request):
  if request.user.is_authenticated:
    cart_items = CartItem.objects.filter(user=request.user)
  else:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)
  subtotal = 0 
  for cart_item in cart_items:
    subtotal += (cart_item.quantity * cart_item.product.price)
  tax = (subtotal * 18) // 100

  context = {
    'cart_items': cart_items,
    'subtotal': subtotal,
    'tax': tax,
  }
  return render(request,'carts/checkout.html',context)


