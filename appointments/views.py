from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Appointment, Timetable
from .serializers import AppointmentSerializer, TimetableSerializer
from .utils import (send_email_for_patient, send_email_for_patient_update, is_valid_appointment_time)


class AppointmentListView(APIView):
    """
    Класс для вывода списка записей к врачу.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: AppointmentSerializer(many=True)},
        tags=["Appointments"]
    )
    def get(self, request):
        """
        Метод для получения списка записей к врачу.
        """
        appointments = Appointment.objects.all()  # Получаем все записи
        serializer = AppointmentSerializer(appointments, many=True)  # Сериализуем данные
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class TimetableListView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: TimetableSerializer(many=True)},
        tags=["Timetables"]
    )
    def get(self, request):

        timetables = Timetable.objects.all()
        serializer = TimetableSerializer(timetables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
