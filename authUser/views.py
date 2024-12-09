from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, DoctorSerializer
from .models import CustomUser

from drf_spectacular.utils import extend_schema


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        parameters=[UserSerializer],
        responses={201: {"message": "User created successfully, please confirm registration"}},
        tags=["Register"],
    )
    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(is_active=True)

            return Response({"message": "User created successfully, please confirm registration"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterConfirmView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={200: UserSerializer(many=True)},
        tags=["Register"],
    )
    def get(self, request, pk, token):
        user = get_object_or_404(CustomUser, pk=pk)

        if confirmation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email successfully verified!"},
                            status=status.HTTP_200_OK)

        return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer()},
        tags=["Users"],
    )
    def get(self, request):
        serializer = UserSerializer(data=request.data)
        user = request.user
        return Response({
            "nickname": user.nickname,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "id": user.id
        })


class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer(many=True)},
        tags=["Users"],
    )
    def get(self, request):
        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: DoctorSerializer(many=True)},
        tags=["Users"],
    )
    def get(self, request):
        doctor = request.doctors
        serializer = DoctorSerializer(doctor, many=True)
        return Response({
            "nickname": doctor.nickname,
            "email": doctor.email,
            "first_name": doctor.first_name,
            "last_name": doctor.last_name,
            "role": doctor.role,
            "id": doctor.id
        })


class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: DoctorSerializer(many=True)},
        tags=["Users"],
    )
    def delete(self, request, pk):
        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        user.delete()
        return Response({"message": "Service deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
