from django.contrib import admin
from .models import Category,SubCategory

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('category_name',)}
  list_display = ['id','category_name','slug']


class SubCategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('name',)}
  list_display = ['name','slug']
# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)