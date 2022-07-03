from django.contrib import admin
from .models import Cart,CartItem,WishList

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)