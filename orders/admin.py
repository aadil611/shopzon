from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.
class OrderProductInline(admin.TabularInline):
  model = OrderProduct
  readonly_fields = ['payment','user','product','quantity','product_price','ordered','variation']
  extra = 0
  

class OrderAdmin(admin.ModelAdmin):
  list_display = ['user','order_number','phone_number','email','order_total','status','is_ordered']
  list_filter = ['status','is_ordered']
  search_fields = ['email','order_number','phone_number','first_name','last_name']
  list_per_page = 20
  inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Order,OrderAdmin)