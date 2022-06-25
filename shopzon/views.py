from django.http import HttpResponse
from django.shortcuts import render
from category.models import Category
from store.models import Product
from random import choices

def home(request):
  categories = Category.objects.all().order_by('category_name')
  new_products = Product.objects.all().order_by('-created_date')[:20]
  deals_of_the_day = new_products[16:]
  new_products = new_products[:16]
  context = {
    'categories': categories,
    'new_products': new_products,
    'deals_of_the_day':deals_of_the_day
  }
  return render(request,'home.html',context)