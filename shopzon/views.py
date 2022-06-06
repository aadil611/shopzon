from django.http import HttpResponse
from django.shortcuts import render
from category.models import Category
from store.models import Product

def home(request):
  categories = Category.objects.all().order_by('category_name')
  new_products = Product.objects.all().order_by('-created_date')[:16]

  context = {
    'categories': categories,
    'new_products': new_products
  }
  return render(request,'home.html',context)