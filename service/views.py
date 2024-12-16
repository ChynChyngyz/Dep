from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .filters import ServicesFilter
from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @extend_schema(
        request=None,
        responses={200: ServiceSerializer(many=True)},
        tags=["Service"],
    )
    def get(self, request):

        filterset = ServicesFilter(request.GET, queryset=Service.objects.all())

        if filterset.is_valid():
            services = filterset.qs.order_by('id')
        else:
            return Response({"count": 0,
                             "next": None,
                             "previous": None,
                             "results": []
                             }, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(services, request)

        serializer = ServiceSerializer(paginated_data, many=True)

        return paginator.get_paginated_response(serializer.data)


class ServiceCreateView(APIView):

    @extend_schema(
        request=ServiceSerializer,
        parameters=[ServiceSerializer],
        responses={201: {"message": "Service created successful"}},
        tags=["Service"],
    )
    def post(self, request):

        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = ServiceSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ServiceSerializer,
        parameters=[ServiceSerializer],
        # parameters=[
        #     OpenApiParameter('title', OpenApiTypes.STR, description='Название', location=OpenApiParameter.PATH, ),
        #     OpenApiParameter('description', OpenApiTypes.STR, description='Описание', location=OpenApiParameter.PATH),
        #     OpenApiParameter('price', OpenApiTypes.STR, description='Цена', location=OpenApiParameter.PATH),
        # ],
        responses={201: {"message": "Service updated successful"}},
        tags=["Service"],
    )
    def put(self, request, pk):
        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ServiceSerializer,
        responses={204: {"message": "Service deleted successful"}},
        tags=["Service"],
    )
    def delete(self, request, pk):
        if request.user.role != 'Admin':
            return Response({"error": "Access denied. Only admin can perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service, data=request.data, partial=True)
        service.delete()
        return Response({"message": "Service deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
