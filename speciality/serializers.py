from drf_spectacular.utils import extend_schema_field
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Speciality


def validate_image(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError("Только файлы форматов .jpg, .jpeg и .png разрешены.")
    return value


class SpecialitySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validate_image], required=False)

    class Meta:
        model = Speciality
        fields = ['id', 'speciality_name', 'description', 'image', 'image_url']

    @extend_schema_field(serializers.URLField)
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    image_url = serializers.SerializerMethodField('get_image_url')

