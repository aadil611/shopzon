from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category,SubCategory
from random import choice,randint
from django.core import serializers
from django.http import HttpResponse
import json

# Create your views here
def products(request,category_slug):
  # subcategory = SubCategory.objects.get(slug=category_slug)
  try:
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
  except:
    subcategory = get_object_or_404(SubCategory,slug=category_slug)
    products = Product.objects.filter(sub_category=subcategory)
  products_count = products.count()
  context = {
    'products': products,
    'products_count': products_count
  }
  return render(request,'products.html',context)



def get_notification(request):
  product = choice(Product.objects.all())
  product = {
    'name': product.name,
    'url' : product.images.url,
    'time': randint(1, 10),
    'href': '/product_details/' + product.slug,
  }
  return HttpResponse(json.dumps(product))


def search(request):
  if request.method == 'GET':
    keyword = request.GET.get('search')
    try:
      category = Category.objects.get(slug=keyword)
      products = Product.objects.filter(category=category)
    except:
      try:
        subcategory = SubCategory.objects.get(slug=keyword)
        products = Product.objects.filter(sub_category=subcategory)
      except:
        products = Product.objects.filter(name__contains=keyword)

    products_count = products.count()
    context = {
      'products':products,
      'products_count':products_count
    }

  return render(request,'products.html',context)


def product_details(request,slug):
  product = get_object_or_404(Product, slug=slug)
  context = {
    'product':product
  }
  return render(request,'product_details.html',context)
