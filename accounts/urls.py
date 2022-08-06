from django.urls import path  
from .views import *

urlpatterns = [
  path('register/',register,name='register'),
  path('login/',login,name='login'),
  path('logout/',logout,name='logout'),
  path('activate/<str:uid64>/<str:token>/',activate,name='activate'),
  path('dashboard/',dashboard,name='dashboard'),
  path('forgot_password/',forgot_password,name='forgot_password'),
  path('reset_password_validate/<str:uidb64>/<str:token>/',reset_password_validate,name='reset_password_validate'),
  path('reset_password/',reset_password,name='reset_password'),
  path('my_orders/',my_orders,name='my_orders'),
  path('my_payments/',my_payments,name='my_payments'),
  path('update_profile/',update_profile,name='update_profile'),
  path('change_password/',change_password,name='change_password'),
]