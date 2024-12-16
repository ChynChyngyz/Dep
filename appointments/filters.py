import django_filters

from .models import Appointment, Timetable
from authUser.models import CustomUser

class AppointmentFilter(django_filters.FilterSet):

    date_created_from = django_filters.DateFilter(field_name='date_created', lookup_expr='gte')
    date_created_to = django_filters.DateFilter(field_name='date_created', lookup_expr='lte')
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    status_of_appointment = django_filters.CharFilter(field_name='status_of_appointment', lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = ['date_created_from', 'date_created_to', 'price_from', 'price_to', 'status_of_appointment']


class TimetableFilter(django_filters.FilterSet):

    doctor = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.filter(role='Doctor'), label="Врач")
    day_of_visit = django_filters.NumberFilter(field_name='day_of_visit', lookup_expr='exact', label="День недели")

    class Meta:
        model = Timetable
        fields = ['doctor', 'day_of_visit']
