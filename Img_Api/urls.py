from django.urls import path
from . import views
from .views import *
from django.urls import include
<<<<<<< HEAD
from .views import *

=======
>>>>>>> 4d07779287d1b468c273939f4173e00c13a1ddae

urlpatterns = [
    path('home', views.index, name='home'),
    path('img_type/', views.create_img_type, name='create_img_type'),
    path('add_img/', views.add_img_withTypeType, name='add_img_withTypeType'),
    path('imgtypes_api/', views.imgtypes_api),
    path('imgsapi/<int:id>' , views.imgsapi),
    path('imgsapia/<int:id>' , views.imgsapia),
    path('imgsapipa/<int:id>' , views.imgsapi_pa),
    # path('snippets/<int:id>/', SnippetsListView.as_view(), name='snippets-list'),
    path('snippetsidpage/<int:ID_Type_id>/', SnippetsListViewWhereidtypeidpa.as_view(), name='snippets-detail'),
<<<<<<< HEAD
=======
    path('snippetsids/<int:ID_Type_id>/', SnippetsListViewWhereidtypeidpa.as_view(), name='snippets-detail'),
>>>>>>> 4d07779287d1b468c273939f4173e00c13a1ddae
    path('imgs_api/', views.no_rest_Imgs_all),
    path('send-notif/', views.send_notification, name='send-notification'),
    path('send-notif-page/', views.send_notification_page, name='send-notification-page'),
    path('imgsapinew/' , views.imgsapi_new),
]