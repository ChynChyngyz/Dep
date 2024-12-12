from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (AppointmentListView, AppointmentCreateView, AppointmentUpdateView, AppointmentCancelView,
                    TimetableListView, TimetableCreateView, TimetableUpdateView, TimetableDeleteView, Weather,
                    CurrencyLayer)

urlpatterns = [
    path('appointment-list/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointment-create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointment-update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointment-delete/<int:pk>/', AppointmentCancelView.as_view(), name='appointment-delete'),

    path('timetable-list/', TimetableListView.as_view(), name='timetable-list'),
    path('timetable-create/', TimetableCreateView.as_view(), name='timetable-create'),
    path('timetable-update/<int:pk>/', TimetableUpdateView.as_view(), name='timetable-update'),
    path('timetable-delete/<int:pk>/', TimetableDeleteView.as_view(), name='timetable-delete'),

    path('weather/<str:city>/', Weather.as_view(), name='weather'),
    path('currency-layer/', CurrencyLayer.as_view(), name='currency-layer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
