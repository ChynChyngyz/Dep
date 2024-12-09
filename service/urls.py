from django.urls import path

from .views import (ServiceListView, ServiceDetailView, ServiceCreateView,
                    ServiceUpdateView, ServiceDeleteView)


urlpatterns = [
    path('service-list', ServiceListView.as_view(), name='service_list'),
    # path('service-info/<int:pk>/', ServiceDetailView.as_view(), name='service_info'),
    # path('speciality-service-info/<int:pk>/', SpecialityServiceListView.as_view(), name='speciality_service'),
    path('create/', ServiceCreateView.as_view(), name='service_create'),
    path('update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete')
]
