# FirebaseStorage/urls.py

from django.urls import path
from .views import *  
from . import views


urlpatterns = [

    path('upload2/', upload_image2, name='upload_image'),
    path('images2/', list_images2, name='list_images'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('list_images/', views.list_images, name='list_images'),

]
