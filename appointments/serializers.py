import datetime

from rest_framework import serializers
from .models import Appointment, Timetable

from authUser.serializers import UserSerializer, DoctorSerializer
from service.serializers import ServiceSerializer


class AppointmentSerializer(serializers.ModelSerializer):

    service_details = ServiceSerializer(many=True, read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'time', 'price', 'status_of_appointment', 'date_created', 'doctor_details', 'service_details', 'user_details']

    def validate_date(self, value):
        if value <= datetime.date.today():
            raise serializers.ValidationError(
                'Запись доступна только на завтра и далее. Вы не можете записаться на сегодня или в прошлое.')
        return value


class TimetableSerializer(serializers.ModelSerializer):

    doctor_details = DoctorSerializer(source='doctor', many=True, read_only=True)

    class Meta:
        model = Timetable
        fields = ['id', 'day_of_visit', 'doctor_details']