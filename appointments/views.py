import requests

from web import settings

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .filters import *
from .models import Appointment, Timetable
from .serializers import AppointmentSerializer, TimetableSerializer
from .utils import (send_email_for_patient, send_email_for_patient_update, is_valid_appointment_time)


class Weather(APIView):

    def get(self, request, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHERMAP_API_KEY}'
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            return JsonResponse({"error": "Weather data not available"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        return JsonResponse(data)


class CurrencyLayer(APIView):

    def get(self, request):
        url = f"http://v6.exchangerate-api.com/v6/{settings.CURRENCYLAYER_API_KEY}/latest/USD"
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            return JsonResponse({"error": "Weather data not available"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        return JsonResponse(data)


class AppointmentListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @extend_schema(
        request=None,
        responses={200: AppointmentSerializer(many=True)},
        tags=["Appointments"]
    )
    def get(self, request):

        filterset = AppointmentFilter(request.GET, queryset=Appointment.objects.all())

        if filterset.is_valid():
            appointments = filterset.qs.order_by('id')
        else:
            return Response({"count": 0,
                             "next": None,
                             "previous": None,
                             "results": []
                             }, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(appointments, request)

        serializer = AppointmentSerializer(paginated_data, many=True)
        return paginator.get_paginated_response(serializer.data)


class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AppointmentSerializer,
        parameters=[AppointmentSerializer],
        responses={201: {"message": "Appointment created successfully"}},
        tags=["Appointments"]
    )
    def post(self, request):
        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            appointment_time = serializer.validated_data.get("time")
            appointment_date = serializer.validated_data.get('date')
            doctor = serializer.validated_data.get('doctor')

            validation_errors = is_valid_appointment_time(appointment_time, doctor, appointment_date)

            if validation_errors:
                return Response({"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST)

            appointment = serializer.save()
            send_email_for_patient(appointment.user.email, appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AppointmentSerializer,
        parameters=[AppointmentSerializer],
        responses={201: {"message": "Appointment updated successfully"}},
        tags=["Appointments"]
    )
    def put(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

        if serializer.is_valid():

            appointment_time = serializer.validated_data.get("time")
            appointment_date = serializer.validated_data.get('date')
            doctor = serializer.validated_data.get('doctor')

            validation_errors = is_valid_appointment_time(appointment_time, doctor, appointment_date)

            if validation_errors:
                return Response({"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST)

            appointment = serializer.save()
            send_email_for_patient_update(appointment.user.email, appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AppointmentSerializer,
        responses={204: {"message": "Appointment deleted successfully"}},
        tags=["Appointments"]
    )
    def delete(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        appointment.delete()
        return Response({"message": "Appointment canceled successfully."}, status=status.HTTP_204_NO_CONTENT)



class AppointmentCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AppointmentSerializer,
        responses={204: {"message": "Appointment canceled successfully"}},
        tags=["Appointments"]
    )
    def delete(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        appointment.canceled()
        return Response({"message": "Appointment canceled successfully."}, status=status.HTTP_204_NO_CONTENT)


class TimetableListView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @extend_schema(
        request=None,
        responses={200: TimetableSerializer(many=True)},
        tags=["Timetables"]
    )
    def get(self, request):

        filterset = TimetableFilter(request.GET, queryset=Timetable.objects.all())

        if filterset.is_valid():
            timetables = filterset.qs.order_by('id')
        else:
            return Response({"count": 0,
                             "next": None,
                             "previous": None,
                             "results": []
                             }, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(timetables, request)

        serializer = TimetableSerializer(paginated_data, many=True)
        return paginator.get_paginated_response(serializer.data)


class TimetableCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TimetableSerializer,
        responses={201: {"message": "Timetable created successfully"}},
        tags=["Timetables"]
    )
    def post(self, request):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        doctor_id = request.data.get('doctor')
        day_of_visit = request.data.get('day_of_visit')

        if Timetable.objects.filter(doctor_id=doctor_id, day_of_visit=day_of_visit).exists():
            return Response(
                {"error": "Расписание для этого врача в этот день уже существует."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TimetableSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimetableUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TimetableSerializer,
        parameters=[OpenApiParameter('days_of_week', OpenApiTypes.INT, description='Дни недели',
                                     location=OpenApiParameter.PATH, )],
        responses={200: {"message": "Timetable updated successfully"}},
        tags=["Timetables"]
    )
    def put(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            timetable = Timetable.objects.get(pk=pk)
        except Timetable.DoesNotExist:
            return Response({"error": "Timetable not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TimetableSerializer(timetable, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimetableDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TimetableSerializer,
        responses={204: {"message": "Timetable deleted successfully"}},
        tags=["Timetables"]
    )
    def delete(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            timetable = Timetable.objects.get(pk=pk)
        except Timetable.DoesNotExist:
            return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)

        timetable.delete()
        return Response({"message": "Timetable deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
