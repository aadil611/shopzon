from django.db import models
from category.models import Category,SubCategory

# Create your models here.
class Product(models.Model):
  name          = models.CharField(max_length=100,unique=True)
  slug          = models.SlugField(max_length=100,unique=True)
  description   = models.TextField(max_length=500,blank=True)
  price         = models.IntegerField()
  images        = models.ImageField(upload_to='photos/products')
  stock         = models.IntegerField()
  is_available  = models.BooleanField(default=True)
  category      = models.ForeignKey(Category,on_delete=models.CASCADE)
  sub_category  = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
  created_date  = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class VariationManager(models.Manager):
  def color(self):
    return super().filter(variation_category='color',is_active=True)

  def size(self):
    return super().filter(variation_category='size',is_active=True)

variation_choices = (
  ('color','color'),
  ('size','size')
)
class Variation(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variation_category = models.CharField(max_length=64,choices=variation_choices)
  variation_value = models.CharField(max_length=64)
  is_active = models.BooleanField(default=True)
  created_date =models.DateTimeField(auto_now_add=True)

  objects = VariationManager()

  def __str__(self):
    return self.variation_value