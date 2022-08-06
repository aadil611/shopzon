from django.urls import path 
from .views import place_order,payment,payment_complete,invoice


urlpatterns = [
  path('place_order/',place_order,name='place_order'),
  path('payment/',payment,name='payment'),
  path('payment_complete/',payment_complete,name='payment_complete'),
  path('invoice/',invoice,name='invoice'),
]