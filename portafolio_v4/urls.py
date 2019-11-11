"""portafolio_v4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include
from faskApp import views
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fask/', include('faskApp.urls', namespace='faskApp')),
    path('',views.home, name='home'),
    path('index1/',views.index, name='home1'),
    path('gg/',views.buscarProducto, name='gg'),
   # path('', include("django.contrib.auth.urls"))
]
handler404 = 'faskApp.views.error_404_view' 
