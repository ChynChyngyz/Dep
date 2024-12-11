import datetime

from rest_framework import serializers
from .models import Appointment, Timetable, ClinicTime

from authUser.serializers import UserSerializer, DoctorSerializer
from authUser.models import CustomUser
from service.serializers import ServiceSerializer


class AppointmentSerializer(serializers.ModelSerializer):

    service_details = ServiceSerializer(many=True, read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'time', 'price', 'status_of_appointment', 'date_created', 'user', 'doctor', 'doctor_details', 'service_details', 'user_details']

    def validate_date(self, value):
        if value <= datetime.date.today():
            raise serializers.ValidationError(
                'Запись доступна только на завтра и далее. Вы не можете записаться на сегодня или в прошлое.')
        return value


class TimetableSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role="Doctor"))

    class Meta:
        model = Timetable
        fields = ['id', 'day_of_visit', 'doctor', 'doctor_details']

    def create(self, validated_data):
        doctor = validated_data.get('doctor')
        day_of_visit = validated_data.get('day_of_visit')

        if Timetable.objects.filter(doctor=doctor, day_of_visit=day_of_visit).exists():
            raise serializers.ValidationError("Расписание для этого врача на этот день уже есть")

        timetable = Timetable.objects.create(doctor=doctor, day_of_visit=day_of_visit)
        return timetable


class ClinicTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicTime
        fields = ['work_start_time', 'work_end_time', 'lunch_start_time', 'lunch_end_time', 'break_start_time', 'break_end_time']
