from rest_framework import serializers
from .models import Service
from authUser.models import CustomUser
from speciality.serializers import SpecialitySerializer
from drf_spectacular.utils import extend_schema_field


class DoctorSerializer(serializers.ModelSerializer):

    speciality = SpecialitySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'nickname', 'phone', 'speciality', 'education', 'description']


class ServiceSerializer(serializers.ModelSerializer):

    doctor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='Doctor'), write_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'doctor', 'doctor_details', 'price', 'description', 'image', 'image_url']

    @extend_schema_field(serializers.URLField)
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    image_url = serializers.SerializerMethodField('get_image_url')
