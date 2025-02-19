from django.shortcuts import render,redirect

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# views.py
from django.conf import settings
from .models import UploadedImage

from django.http import JsonResponse
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from django.core.files.storage import default_storage
from .models import UserProfile
import json
from django.views import View

  # ??????? ??? FCM ?? ??? fcm.py

# ??????? ???? ???????


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    base_url = "http://www.sarrawi.com"
    
    if request.method == 'POST':
        image = request.FILES.get('image')  # ?????? ??? ?????? ?? ??? request
        if image:
            # ??? ?????? ???????? default_storage
            file_name = default_storage.save(f'profile_imagesFirebase/{image.name}', image)
            file_url = f"{base_url}{settings.MEDIA_URL}{file_name}"
            
            # ????? ?????? ?? ????? ????????
            UploadedImage.objects.create(image_url=file_url)
            
            return Response({'message': 'Image uploaded successfully!', 'image_url': file_url}, status=status.HTTP_201_CREATED)
        return Response({'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        
@api_view(['GET'])
def list_images(request):
    images = UploadedImage.objects.all()  # ?????? ??? ???? ????? ?? ????? ????????
    
    image_data = []
    for image in images:
        image_data.append({
            'image_url': image.image_url
        })
    
    return Response({'images': image_data}, status=status.HTTP_200_OK)
        




@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image2(request):
    base_url = "http://www.sarrawi.com"

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            file_name = default_storage.save(f'profile_imagesFirebase/{image.name}', image)
            file_url = f"{base_url}{settings.MEDIA_URL}{file_name}"

            # ??? ???? ?????? ?? ????? ????????
            UploadedImage.objects.create(image_url=file_url)

            return redirect('list_images')

    return render(request, 'upload_image.html')


def list_images2(request):
    images = UploadedImage.objects.all()  # ??? ????? ???????? ?? ????? ????????

    return render(request, 'list_images.html', {'images': images})

