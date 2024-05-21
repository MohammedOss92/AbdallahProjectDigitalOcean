from django.urls import path
from . import views
from .views import *
from django.urls import include


urlpatterns = [
path('nokatapi/', SnippetsListViews.as_view(), name='snippets-list'),
path('nokatin/', generics_list_Nokat.as_view(), name='snippets-list'),
path('nokatup/<int:pk>', generics_pk_Nokat.as_view(), name='snippets-list'),
path('add_image_nokat/', views.add_image_nokat, name='add_imgs'),
path('imgnokatapi/', SnippetsListView.as_view(), name='snippets-list'),
path('imgnokatup/<int:pk>', generics_pk_imgNokat.as_view(), name='snippets-list'),
path('imgsNokatapiold/', views.imgsNokatapi, name='add_imgs'),



]

