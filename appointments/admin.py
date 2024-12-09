from django.contrib import admin

from .models import Appointment, Timetable


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Класс для настройки панели администратора модели Запись.
    """

    list_display = ('user', 'doctor', 'status_of_appointment',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """
    Класс для настройки панели администратора модели Запись.
    """

    list_display = ('day_of_visit',)
