from rest_framework import serializers
from .models import Convert
class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        fields = ['file']

class ConvertSerializerLoc(serializers.ModelSerializer):
    class Meta:
        model = Convert
        fields = '__all__'