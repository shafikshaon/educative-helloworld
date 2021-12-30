from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
