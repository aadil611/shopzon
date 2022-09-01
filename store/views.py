from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,ReviewRating,StockNotification
from accounts.models import UserProfile
from carts.models import Cart,CartItem,WishList
from carts.views import _cart_id
from category.models import Category,SubCategory
from random import choice,randint
from django.core import serializers
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import ReviewRatingForm
from orders.models import OrderProduct
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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

  try:
    purchased = OrderProduct.objects.filter(user__id=request.user.id,product__slug=slug).exists()
    reviews = ReviewRating.objects.filter(product=product)
  except OrderProduct.DoesNotExist:
    purchased = None

  average = ReviewRating.objects.filter(product=product,status=True).aggregate(avg=Avg('rating'))
  avg = 0 
  if average['avg'] is not None:
    if average['avg'] > 0:
      avg = float(average['avg'])

  try:
    user_profile = UserProfile.objects.filter(user=request.user)
  except:
    user_profile = None

  try:
    notification_count = StockNotification.objects.filter(user=request.user,product=product,is_sent=True).count()
    is_notify_me  = StockNotification.objects.filter(user=request.user,product=product,is_sent=False).exists()
  except:
    notification_count = None
    is_notify_me = None

  context = {
    'product'               : product,
    'in_stock'              : in_stock,
    'in_wishlist'           : in_wishlist,
    'in_cart'               : in_cart,
    'variations'            : variations,
    'purchased'             : purchased,
    'reviews'               : reviews,
    'avg_rating'            : avg,
    'user_profile'          : user_profile,
    'notify_me'             : is_notify_me,
    'notification_count'    : notification_count
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


def submit_review(request):
  if request.method == 'POST':
    try:
        review = ReviewRating.objects.get(user__id=request.user.id,product__id=request.POST['product_id'])
        form = ReviewRatingForm(request.POST,instance=review)
        form.save()
        messages.success(request,'Review Updated successfully')
    except:
      form = ReviewRatingForm(request.POST)
      if form.is_valid():
        review = ReviewRating()
        review.user_id = request.user.id
        review.product_id = request.POST.get('product_id')
        review.subject = form.cleaned_data['subject']
        review.review = form.cleaned_data['review']
        review.rating = form.cleaned_data['rating']
        review.ip = request.META.get('REMOTE_ADDR')
        review.save()
        messages.success(request,'Review submitted successfully')

  return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def notify_me(request,product_id):
  product = get_object_or_404(Product,id=product_id)
  try:
    notification = StockNotification.objects.get(user=request.user,product=product,is_sent=False)
    notification.delete()
  except:
    StockNotification.objects.create(user=request.user,product=product)
  return redirect(reverse('product_details',args=[product.slug,]))

