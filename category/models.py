from django.db import models

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

class SubCategory(models.Model):
  category    = models.ForeignKey(Category,on_delete=models.CASCADE)
  name        = models.CharField(max_length=100,unique=True)
  slug        = models.SlugField(max_length=100,unique=True)
  image       = models.ImageField(upload_to = 'photos/categories/subcategories',blank=True)

  class Meta:
    verbose_name          = 'subcategory'
    verbose_name_plural   = 'subcategories'

  def __str__(self):
    return self.name