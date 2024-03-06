from django.shortcuts import render
from .serializer import SnippetsDetailSerializer
from django.http import HttpResponse
import requests
import json
from django.http.response import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import *
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # عدد العناصر في الصفحة
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # عدد الصفحات الكلي
            'current_page': self.page.number,  # رقم الصفحة الحالية
            'results': data
        })

class SnippetsListView(ListAPIView):
    serializer_class = SnippetsDetailSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # استخدم filter بدلاً من exclude
        return Nokat.objects.exclude(new_msgs_text=1).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # استخدم super للحصول على الاستجابة من الفئة الأم
        return super().list(request, *args, **kwargs, data={"NokatsModel": serializer.data})
    

class generics_list_Nokat(generics.ListCreateAPIView):
    queryset = Nokat.objects.all()
    serializer_class = SnippetsDetailSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class generics_pk_Nokat(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nokat.objects.all()
    serializer_class = SnippetsDetailSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



