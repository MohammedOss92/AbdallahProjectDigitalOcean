from django.urls import path
from . import views
from django.urls import include
from .views import *





urlpatterns = [
    
   
#6.1 GET POST from rest framework class based view generics
    path('genericsmsgstypes/<int:pk>', views.generics_pk_msgstypes.as_view()),
    path('genericsmsgstypes/', views.generics_list_msgstypes.as_view()),
    path('genericsmsgs/', views.generics_msgs.as_view()),
    path('generics_pk_msgs/<int:pk>', views.generics_pk_msgs.as_view()),
    #2
    path('send-notification/', views.send_notification, name='send-notification'),
    path('send-notification-page/', views.send_notification_page, name='send-notification-page'),
        ####################

    path('messages/<int:id>/', views.AllInfoRelatedToIDView.as_view(), name='message-detail'),
    path('msgsapishow/<int:id>' , views.msgsapi_show),
    path('msgtypes_api_show/', views.msgtypes_api_show),
    path('snippetsids/<int:ID_Type_id>/', SnippetsListViewWhereidtypeidpa.as_view(), name='snippets-detail'),
    path('msgstypespa/', SnippetsListViewsMsgssType.as_view(), name='snippets-list'),
    path('msgsapiidspa/<int:ID_Type_id>', SnippetsMsgssWhereTID.as_view(), name='snippets-list'),
   
  


    
]
