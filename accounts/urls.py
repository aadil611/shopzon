from django.urls import path  
from .views import register,login,logout,activate,dashboard,forgot_password,reset_password_validate,reset_password

urlpatterns = [
  path('register/',register,name='register'),
  path('login/',login,name='login'),
  path('logout/',logout,name='logout'),
  path('activate/<str:uid64>/<str:token>/',activate,name='activate'),
  path('dashboard/',dashboard,name='dashboard'),
  path('',dashboard,name='dashboard'),
  path('forgot_password/',forgot_password,name='forgot_password'),
  path('reset_password_validate/<str:uidb64>/<str:token>/',reset_password_validate,name='reset_password_validate'),
  path('reset_password/',reset_password,name='reset_password'),
]