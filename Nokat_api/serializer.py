from rest_framework import serializers
from Nokat_api.models import * 




class SnippetsDetailSerializer(serializers.ModelSerializer):

  class Meta:
    model = Nokat
    fields = '__all__'
    # fields = ['id', 'ID_Type', 'pic', 'new_img','image_url']


    


class SnippetsDetailSerializers(serializers.ModelSerializer):

  class Meta:
    model = ImagesNokat
    fields = '__all__'