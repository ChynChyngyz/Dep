import django_filters

from .models import Speciality

class SpecialitiesFilter(django_filters.FilterSet):

    speciality_name = django_filters.CharFilter(field_name='speciality_name', lookup_expr='icontains', label="Название сервиса")
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label="Описание сервиса")

    class Meta:
        model = Speciality
        fields = ['speciality_name', 'description']
