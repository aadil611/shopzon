import time
from random import choice
from store.models import Product


def notification(request):
  product = choice(Product.objects.all())
  return dict(product=product)