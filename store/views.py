from django.shortcuts import render
from .models import Product
from random import choice,randint
from django.core import serializers
from django.http import HttpResponse
import json

# Create your views here
def get_notification(request):
  product = choice(Product.objects.all())
  product = {
    'name': product.name,
    'url' : product.images.url,
    'time': randint(0, 10),
  }
  return HttpResponse(json.dumps(product))