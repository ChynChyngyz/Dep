from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Класс для настройки панели администратора модели Услуга.
    """

    list_display = ('title', 'get_specialities', 'price',)
