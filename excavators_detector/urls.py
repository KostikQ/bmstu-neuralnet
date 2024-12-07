from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from neuralnet import settings
from . import views

app_name = 'excavators_detector'
urlpatterns = [
    path('', views.image_upload_view, name='index'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)