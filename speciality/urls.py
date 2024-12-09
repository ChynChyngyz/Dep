from django.urls import path
from .views import (SpecialityListView, SpecialityCreateView, SpecialityUpdateView,
                    SpecialityDeleteView)

urlpatterns = [
    path('speciality-list/', SpecialityListView.as_view(), name='speciality_list'),  # список специализаций
    path('create/', SpecialityCreateView.as_view(), name='speciality_create'),  # создание специализации
    path('update/<int:pk>/', SpecialityUpdateView.as_view(), name='speciality_update'),  # редактирование специализации
    path('delete/<int:pk>/', SpecialityDeleteView.as_view(), name='speciality_delete'),  # удаление специализации
]
