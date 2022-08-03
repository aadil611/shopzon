from django.urls import path 
from .views import *

urlpatterns = [
  path('get_notification/',get_notification),
  path('products/<slug:category_slug>/',products,name='products'),
  path('search/',search,name='search'),
  path('product_details/<slug:slug>/',product_details,name='product_details'),
  path('get_cart_variations/<int:product_id>/',get_cart_variations,name='get_cart_variations'),
  path('submit_review/',submit_review,name='submit_review')
]