import django_filters

from .models import Service
from authUser.models import CustomUser

class ServicesFilter(django_filters.FilterSet):

    doctor = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.filter(role='Doctor'), label="Врач")
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label="Название услуги")
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label="Описание услуги")
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label="Цена от")
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label="Цена до")

    class Meta:
        model = Service
        fields = ['doctor', 'title', 'price_from', 'price_to', 'description']
