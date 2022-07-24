from django.contrib import admin
from .models import Cart,CartItem,WishList

class CartAdmin(admin.ModelAdmin):
  list_display = ['cart_id','date_added']
# Register your models here.
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem)
admin.site.register(WishList)