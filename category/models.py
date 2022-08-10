from django.db import models
from store.models import Product

# Create your models here.
class Category(models.Model):
  category_name   = models.CharField(max_length=100,unique=True)
  slug            = models.SlugField(max_length=100,unique=True)
  description     = models.TextField(max_length=255,blank=True)
  cat_image       = models.ImageField(upload_to = 'photos/categories',blank=True)

  class Meta:
    verbose_name          = 'category'
    verbose_name_plural   = 'categories'

  def __str__(self):
    return self.category_name

  def subcategories(self):
    subcat = SubCategory.objects.filter(category__id=self.id)
    return subcat

  def product_count(self):
    products = Product.objects.filter(category__id=self.id)
    return products.count()

class SubCategory(models.Model):
  SUITED_FOR = (
    ('male','male'),
    ('female','female'),
    ('both','both'),
    ('any','any'),
  )

  category    = models.ForeignKey(Category,on_delete=models.CASCADE)
  name        = models.CharField(max_length=100,unique=True)
  slug        = models.SlugField(max_length=100,unique=True)
  image       = models.ImageField(upload_to = 'photos/categories/subcategories',blank=True)
  suited_for  = models.CharField(max_length=16,blank=True,default='any',choices=SUITED_FOR)

  class Meta:
    verbose_name          = 'subcategory'
    verbose_name_plural   = 'subcategories'

  def __str__(self):
    return self.name