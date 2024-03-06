from django.urls import path
from . import views
from .views import *
from django.urls import include


urlpatterns = [
path('nokatapi/', SnippetsListView.as_view(), name='snippets-list'),
path('nokatin/', generics_list_Nokat.as_view(), name='snippets-list'),
path('nokatup/<int:pk>', generics_pk_Nokat.as_view(), name='snippets-list'),



]

