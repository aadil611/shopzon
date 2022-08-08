from django.urls import path 
from .views import *

urlpatterns = [
  path('cart/',cart,name='cart'),
  path('add_cart/<int:product_id>/',add_cart,name='add_cart'),
  path('minus_cart/<int:product_id>/<int:cart_item_id>/',minus_cart,name='minus_cart'),
  path('remove_cart/<int:product_id>/<int:cart_item_id>/',remove_cart,name='remove_cart'),
  path('wishlist/<int:product_id>/',add_wishlist,name='wishlist'),
  path('show_wishlist/',show_wishlist,name='show_wishlist'),
  path('remove_wishlist/<int:product_id>/',remove_wishlist,name='remove_wishlist'),
  path('checkout/',checkout,name='checkout'),
  path('move_to_cart/<int:product_id>/',move_to_cart,name='move_to_cart'),
  path('move_to_wishlist/<int:cart_item_id>/',move_to_wishlist,name='move_to_wishlist')
]