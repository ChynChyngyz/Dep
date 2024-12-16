from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import CustomUser
from .filters import UsersFilter
from .utils import confirmation_token
from .serializers import UserSerializer, DoctorSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


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

            token = confirmation_token.make_token(user)

            confirmation_register_url = request.build_absolute_uri(
                reverse('register_confirm', kwargs={'pk': user.pk, 'token': token})
            )

            send_mail(
                subject="Please confirm registration!",
                message=f"Hi, {user.nickname}! Follow this link {confirmation_register_url}",
                from_email="Bicos-Abricos@yandex.ru",
                recipient_list=[user.email, ]
            )
            print(f"qwerty {user.email}")
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


class PasswordReset(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={200: {"message": "Password reset link sent to your email"}},
        tags=["Password"],
    )
    def post(self, request):
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = confirmation_token.make_token(user)

            reset_password_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'pk': user.pk, 'token': token})
            )

            send_mail(
                subject="Password Reset Request",
                message=f"Hi, {user.nickname}! To reset your password, follow this link: {reset_password_url}",
                from_email="Bicos-Abricos@yandex.ru",
                recipient_list=[user.email],
            )
            return Response({"message": "Password reset link sent to your email"}, status=status.HTTP_200_OK)

        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        parameters=[OpenApiParameter('new_password', OpenApiTypes.STR, description='Новый пароль',
                                     location=OpenApiParameter.PATH, )],
        responses={201: {"message": "Password reset successful!"}},
        tags=["Password"],
    )
    def post(self, request, token, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        if not confirmation_token.check_token(user, token):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("new_password")

        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful!"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Try again"}, status=status.HTTP_400_BAD_REQUEST)


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
    pagination_class = PageNumberPagination

    @extend_schema(
        request=None,
        responses={200: UserSerializer(many=True)},
        tags=["Users"],
    )
    def get(self, request):
        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        filterset = UsersFilter(request.GET, queryset=CustomUser.objects.all())

        if filterset.is_valid():
            users = filterset.qs.order_by('id')
        else:
            return Response({"count": 0,
                             "next": None,
                             "previous": None,
                             "results": []
                             }, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(paginated_data, many=True)

        return paginator.get_paginated_response(serializer.data)


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
