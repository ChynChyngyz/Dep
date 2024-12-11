from django.contrib import admin

from .models import Appointment, Timetable, ClinicTime


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = ('user', 'doctor', 'status_of_appointment',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):

    list_display = ('day_of_visit',)

    # # Поиск по врачу
    # search_fields = ['doctor__username', 'doctor__first_name', 'doctor__last_name']
    #
    # # Добавим фильтрацию по врачу и дню недели
    # list_filter = ('doctor', 'day_of_week')
    #
    # # Если нужно, можно установить сортировку по дню недели или врачу
    # ordering = ['doctor', 'day_of_week']


@admin.register(ClinicTime)
class ClinicTimeAdmin(admin.ModelAdmin):
    list_display = (
        'work_start_time',
        'work_end_time',
        'lunch_start_time',
        'lunch_end_time',
        'break_start_time',
        'break_end_time'
    )

    list_filter = ('work_start_time', 'work_end_time')

    ordering = ['work_start_time']

    fieldsets = (
        (None, {
            'fields': (
                'work_start_time',
                'work_end_time',
                'lunch_start_time',
                'lunch_end_time',
                'break_start_time',
                'break_end_time'
            )
        }),
    )
