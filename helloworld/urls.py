from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', views.index),
]
