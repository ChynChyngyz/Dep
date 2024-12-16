import django_filters

from .models import CustomUser

class UsersFilter(django_filters.FilterSet):

    doctor = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.filter(role='Doctor'), label="Врач")
    user = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.filter(role='User'), label="Клиент")
    admin = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.filter(role='Admin'), label="Админ")
    nickname = django_filters.CharFilter(field_name='nickname', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    role = django_filters.CharFilter(field_name='role', lookup_expr='icontains')
    date_of_birth = django_filters.DateFromToRangeFilter()

    class Meta:
        model = CustomUser
        fields = ['doctor', 'user', 'admin', 'nickname', 'phone',
                  'first_name', 'last_name', 'role', 'date_of_birth']

