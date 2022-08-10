from django.http import HttpResponse
from django.shortcuts import render
from category.models import Category
from store.models import Product,ReviewRating
from orders.models import OrderProduct
from random import choice

def home(request):
  categories = Category.objects.all().order_by('category_name')
  new_products = Product.objects.all().order_by('-created_date')[:20]
  deals_of_the_day = new_products[16:]
  new_products = new_products[:16]

  top_reviews = ReviewRating.objects.all().order_by('-rating')[:8]
  top_rated_products_ids = []
  for review in top_reviews:
    top_rated_products_ids.append(review.product.id)
  top_rated_products = Product.objects.filter(id__in=top_rated_products_ids)

  recent_orders = OrderProduct.objects.all().order_by('-created_at')
  recent_order_product_ids = set()
  for order in recent_orders:
    recent_order_product_ids.add(order.product.id)

  trending_products = Product.objects.filter(id__in=recent_order_product_ids)[:8]

  context = {
    'categories': categories,
    'new_products': new_products,
    'deals_of_the_day':deals_of_the_day,
    'product': choice(Product.objects.all()),
    'top_rated_products':top_rated_products,
    'new_arrivals':new_products[:8],
    'trending_products':trending_products,
  }
  return render(request,'home.html',context)