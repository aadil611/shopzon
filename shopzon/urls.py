"""shopzon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include 
from .import views
from django.conf import settings
from django.conf.urls.static import static
from category.views import get_sub_category
from store import urls as storeurls
from utils import views as utilsviews

urlpatterns = [
    path('secure_admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('get_sub_category/',get_sub_category),
    path('get_countdown/',utilsviews.get_countdown),
    path('store/',include(storeurls)),
    path('carts/',include('carts.urls')),
    path('accounts/',include('accounts.urls')),
    path('orders/',include('orders.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
