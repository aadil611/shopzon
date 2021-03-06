from django.shortcuts import render,get_object_or_404
from .models import Product
from carts.models import Cart,CartItem,WishList
from carts.views import _cart_id
from category.models import Category,SubCategory
from random import choice,randint
from django.core import serializers
from django.http import HttpResponse
from django.core.paginator import Paginator
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
  paginator = Paginator(products,8)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)
  context = {
    'products': paged_products,
    'products_count': products_count
  }
  return render(request,'store/products.html',context)



def get_notification(request):
  product = choice(Product.objects.all())
  product = {
    'name': product.name,
    'url' : product.images.url,
    'time': randint(1, 10),
    'href': '/store/product_details/' + product.slug,
  }
  return HttpResponse(json.dumps(product))


def search(request):
  if request.method == 'GET':
    keyword = request.GET.get('search','')
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
    paginator = Paginator(products,8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
      'products':paged_products,
      'products_count':products_count,
      'keyword':keyword if len(keyword) > 0 else None
    }

  return render(request,'store/products.html',context)


def product_details(request,slug):
  product = get_object_or_404(Product, slug=slug)
  in_stock = True if product.stock >= 1 else False
  try:
    cart = Cart.objects.get(cart_id = _cart_id(request))
  except Cart.DoesNotExist:
    cart = Cart.objects.create(cart_id = _cart_id(request))

  in_wishlist = True if WishList.objects.filter(cart=cart,product=product).exists() else False
  in_cart     = True if CartItem.objects.filter(cart=cart,product=product).exists() else False
  cart_items = CartItem.objects.filter(cart=cart,product=product)

  variations =[]
  for cart_item in cart_items:
    for variation in cart_item.variation.all():
      variations.append(variation)
  
  context = {
    'product':product,
    'in_stock':in_stock,
    'in_wishlist':in_wishlist,
    'in_cart':in_cart,
    'variations':variations,
  }
  return render(request,'store/product_details.html',context)


def get_cart_variations(request,product_id):
  product = Product.objects.get(id=product_id)
  cart_items = []
  variations = []
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart,product=product)

    for cart_item in cart_items:
      for variation in cart_item.variation.all():
        variations.append(variation.variation_value)
        print(variation.variation_value)
  except:
    pass
  print(variations)
  return HttpResponse(json.dumps({'variations':variations}),content_type='application/json')