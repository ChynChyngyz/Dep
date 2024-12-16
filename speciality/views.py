from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated  # , IsAdminUser

from .filters import SpecialitiesFilter
from .models import Speciality
from .serializers import SpecialitySerializer


class SpecialityListView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @extend_schema(
        request=None,
        responses={200: SpecialitySerializer(many=True)},
        tags=["Speciality"],
    )
    def get(self, request):

        filterset = SpecialitiesFilter(request.GET, queryset=Speciality.objects.all())

        if filterset.is_valid():
            specialities = filterset.qs.order_by('id')
        else:
            return Response({"count": 0,
                             "next": None,
                             "previous": None,
                             "results": []
                             }, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(specialities, request)

        serializer = SpecialitySerializer(paginated_data, many=True)

        return paginator.get_paginated_response(serializer.data)


class SpecialityCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SpecialitySerializer,
        parameters=[SpecialitySerializer],
        responses={201: {"message": "Speciality created successful"}},
        tags=["Speciality"],
    )
    def post(self, request):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = SpecialitySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialityUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SpecialitySerializer,
        parameters=[SpecialitySerializer],
        responses={201: {"message": "Speciality updated successful"}},
        tags=["Speciality"],
    )
    def put(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            speciality = Speciality.objects.get(pk=pk)
        except Speciality.DoesNotExist:
            return Response({"error": "Speciality not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpecialitySerializer(speciality, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialityDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SpecialitySerializer,
        parameters=[OpenApiParameter('id', OpenApiTypes.INT, description='ID специализации', location=OpenApiParameter.PATH)],
        responses={204: {"message": "Speciality deleted successful"}},
        tags=["Speciality"],
    )
    def delete(self, request, pk):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            speciality = Speciality.objects.get(pk=pk)
        except Speciality.DoesNotExist:
            return Response({"error": "Speciality not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpecialitySerializer(speciality, data=request.data, partial=True)
        speciality.delete()
        return Response({"message": "Speciality deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
