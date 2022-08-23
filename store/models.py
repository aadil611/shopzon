from django.db import models
# from category.models import Category,SubCategory
from accounts.models import Account,UserProfile
from django.db.models import Avg
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

# Create your models here.
class Product(models.Model):
  name          = models.CharField(max_length=100,unique=True)
  slug          = models.SlugField(max_length=100,unique=True)
  description   = models.TextField(max_length=500,blank=True)
  price         = models.IntegerField()
  images        = models.ImageField(upload_to='photos/products')
  stock         = models.IntegerField()
  is_available  = models.BooleanField(default=True)
  category      = models.ForeignKey('category.Category',on_delete=models.CASCADE)
  sub_category  = models.ForeignKey('category.SubCategory',on_delete=models.CASCADE)
  created_date  = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


  def review_count(self):
    return ReviewRating.objects.filter(product=self,status=True).count()

  def avg_rating(self):
    average = ReviewRating.objects.filter(product=self,status=True).aggregate(avg=Avg('rating'))
    avg = 0 
    if average['avg'] is not None:
      if average['avg'] > 0:
        avg = float(average['avg'])
    return avg

  def save(self,*args,**kwargs):
    super().save(*args,**kwargs)
    if self.stock > 0:
      channel_layer = get_channel_layer() 
      notifications = StockNotification.objects.filter(product=self,is_sent=False)

      for notification in notifications:
        msg = self.name + ' is back in stock'
        async_to_sync(channel_layer.group_send)(
          notification.user.username,
          {
            'type':'send_notification',
            'message':json.dumps({'message':msg,'slug':self.slug})
          }
        )
        notification.is_sent = True
        notification.save()


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


class ReviewRating(models.Model):
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  subject = models.CharField(max_length=128,blank=True)
  review = models.TextField(max_length=512,blank=True)
  rating = models.FloatField()
  ip = models.CharField(max_length=20,blank=True)
  status = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.subject

  def profile(self):
    try:
      profile = UserProfile.objects.get(user = self.user)
    except:
      profile = None
    return profile

class ProductGallery(models.Model):
  product = models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
  image = models.ImageField(upload_to='store/products',max_length=255)

  def __str___(self):
    return self.product.name

  class Meta:
    verbose_name = 'product gallery'
    verbose_name_plural = 'product galleries'


class StockNotification(models.Model):
  user          = models.ForeignKey(Account, on_delete=models.CASCADE)
  product       = models.ForeignKey(Product, on_delete=models.CASCADE)
  is_sent       = models.BooleanField(default=False)
  created_at    = models.DateTimeField(auto_now_add=True)

