from django.contrib import admin
from .models import Product,Variation,ReviewRating,ProductGallery,StockNotification
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
  model = ProductGallery
  extra = 1
class ProductAdmin(admin.ModelAdmin):
  list_display = ['name','slug','price','stock','category','modified_date','is_available']
  prepopulated_fields = {'slug':('name',)}
  inlines = [ProductGalleryInline,]
class VariationAdmin(admin.ModelAdmin):
  list_display = ('product','variation_value','variation_category','is_active')  
  list_filter  = ('variation_category','variation_value')
  list_editable = ('is_active',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(StockNotification)