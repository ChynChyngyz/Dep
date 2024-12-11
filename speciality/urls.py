from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (SpecialityListView, SpecialityCreateView, SpecialityUpdateView,
                    SpecialityDeleteView)

urlpatterns = [
    path('speciality-list/', SpecialityListView.as_view(), name='speciality_list'),
    path('create/', SpecialityCreateView.as_view(), name='speciality_create'),
    path('update/<int:pk>/', SpecialityUpdateView.as_view(), name='speciality_update'),
    path('delete/<int:pk>/', SpecialityDeleteView.as_view(), name='speciality_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
