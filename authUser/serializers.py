from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from speciality.serializers import SpecialitySerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    doctor_speciality = SpecialitySerializer(source='speciality', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'is_staff', 'avatar', 'nickname', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth',
                  'password', 'speciality', 'doctor_speciality', 'education', 'description', 'experience', 'role']

    @staticmethod
    def create(validated_data, **kwargs):
        password = validated_data.pop('password')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        validated_data.setdefault('role', 'User')
        user = get_user_model().objects.create_user(password=password, **validated_data)
        return user

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if instance.role != 'Doctor':
            data.pop('doctor_speciality', None)

        return data


class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    doctor_speciality = SpecialitySerializer(source='speciality', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'is_staff', 'avatar', 'nickname', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth',
                  'password', 'speciality', 'doctor_speciality', 'education', 'description', 'experience', 'role']

    @staticmethod
    def create(validated_data, **kwargs):
        password = validated_data.pop('password')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        validated_data.setdefault('role', 'Doctor')
        user = get_user_model().objects.create_user(password=password, **validated_data)
        return user
