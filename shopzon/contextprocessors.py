import time
from random import choice
from store.models import Product
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from category.models import Category
from carts.views import _cart_id
from carts.models import Cart, CartItem, WishList
from store.models import StockNotification

channel_layer = get_channel_layer()

# def notification(request):
#   while(True):
#     product = choice(Product.objects.all())
#     # product = {'product': product}
#     async_to_sync(channel_layer.group_send)(
#       'notification_group',
#       {
#         'type':'send_notification',
#         'product':product,
#       }
#     )
#     return product


def cart_count(request):
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except:
    cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

  if request.user.is_authenticated:
    cart_items = CartItem.objects.filter(user=request.user)
  else:
    cart_items = CartItem.objects.filter(cart=cart)
  count = 0
  for cart_item in cart_items:
    count += cart_item.quantity
  context = {"cart_count": count}
  return context


def wishlist_count(request):
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except:
    cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
  wishlist = WishList.objects.filter(cart=cart)
  context = {"wishlist_count": wishlist.count()}
  return context


def categories(request):
  categories = Category.objects.all().order_by("id")
  # categories = dict({'categories':categories})
  context = {"categories": categories}
  return context


def notifications(request):
  notifications = StockNotification.objects.filter(user=request.user.id).order_by('created_at')
  notification_count = notifications.count()
  if notification_count > 5:
    cnt = 0
    for notification in notifications:
      if cnt < (notification_count - 5):
        notification.delete()
      else:
        break
      cnt += 1 

  context = {"notifications": notifications}
  return context