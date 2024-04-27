from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .serializer import *
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
from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from .forms import ImgsFormss
from rest_framework.decorators import api_view
import logging

# Create your views here.



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # ⁄œœ «·⁄‰«’— ›Ì «·’›Õ…
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ⁄œœ «·’›Õ«  «·ﬂ·Ì
            'current_page': self.page.number,  # —ﬁ„ «·’›Õ… «·Õ«·Ì…
            'results': {"NokatModel": data}  #  ⁄œÌ· Â‰« ·Ê÷⁄ "NokatModel"  Õ  "results"
        })


class SnippetsListViews(ListAPIView):
    serializer_class = SnippetsDetailSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        # «” Œœ„ exclude ·«” »⁄«œ «·”Ã·«  «· Ì  Õ ÊÌ ⁄·Ï new_msgs_text »ﬁÌ„… 1
        return Nokat.objects.exclude(new_msgs_text=1).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"NokatModel": serializer.data})

    

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



@staff_member_required
def add_image_nokats(request):
    uploaded_image_urls = []

    if request.method == 'POST':
        form = ImgsFormss(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('pic')
            for image_file in images:
                img_instance = ImagesNokat(pic=image_file)
                img_instance.save()
                uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
                img_instance.image_url = uploaded_image_url
                img_instance.save()
                uploaded_image_urls.append(uploaded_image_url)
    else:
        form = ImgsFormss()

    return render(request, 'aa/addimgs.html', {'form': form, 'uploaded_image_urls': uploaded_image_urls})

def add_image_nokat(request):
    uploaded_image_urls = []

    if request.method == 'POST':
        images = request.FILES.getlist('pic')
        for image_file in images:
            new_img = request.POST.get('new_img')
            img_show = request.POST.get('img_show')
            
            img_instance = ImagesNokat(pic=image_file, new_img=new_img, img_show=img_show)
            img_instance.save()
            
            uploaded_image_url = request.build_absolute_uri(img_instance.pic.url)
            img_instance.image_url = uploaded_image_url
            img_instance.save()
            
            uploaded_image_urls.append(uploaded_image_url)

    return render(request, 'aa/addimgs.html', {'uploaded_image_urls': uploaded_image_urls})




class generics_pk_imgNokat(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImagesNokat.objects.all()
    serializer_class = SnippetsDetailSerializers
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # ⁄œœ «·⁄‰«’— ›Ì «·’›Õ…
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,  # ⁄œœ «·’›Õ«  «·ﬂ·Ì
            'current_page': self.page.number,  # —ﬁ„ «·’›Õ… «·Õ«·Ì…
            'results': {"ImgsNokatModel": data}  #  ⁄œÌ· Â‰« ·Ê÷⁄ "NokatModel"  Õ  "results"
        })


class SnippetsListView(ListAPIView):
    serializer_class = SnippetsDetailSerializers
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        # «” Œœ„ exclude ·«” »⁄«œ «·”Ã·«  «· Ì  Õ ÊÌ ⁄·Ï new_msgs_text »ﬁÌ„… 1
        return ImagesNokat.objects.exclude(img_show=1).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"ImgsNokatModel": serializer.data})

