from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, AppointmentUpdateView, AppointmentCancelView
from .views import TimetableListView, TimetableCreateView, TimetableUpdateView, TimetableDeleteView

urlpatterns = [
    path('appointment-list/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointment-create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointment-update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointment-delete/<int:pk>/', AppointmentCancelView.as_view(), name='appointment-delete'),

    path('timetable-list/', TimetableListView.as_view(), name='timetable-list'),
    path('timetable-create/', TimetableCreateView.as_view(), name='timetable-create'),
    path('timetable-update/<int:pk>/', TimetableUpdateView.as_view(), name='timetable-update'),
    path('timetable-delete/<int:pk>/', TimetableDeleteView.as_view(), name='timetable-delete'),
]
