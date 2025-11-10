from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Service, Booking
from .serializers import (
    ServiceListSerializer, ServiceDetailSerializer,
    BookingSerializer, BookingCreateSerializer
)
from django.db.models import Q


class ServiceListAPIView(APIView):

    @classmethod
    def get(cls, request):
        service_type = request.GET.get('service_type')
        queryset = Service.objects.filter(is_active=True)

        if service_type:
            queryset = queryset.filter(service_type=service_type)

        serializer = ServiceListSerializer(queryset, many=True)
        return Response(serializer.data)


class ServiceDetailAPIView(APIView):

    @classmethod
    def get(cls, request, pk):
        service = get_object_or_404(Service, pk=pk, is_active=True)
        serializer = ServiceDetailSerializer(service)
        return Response(serializer.data)


class BookingCreateAPIView(APIView):
    @classmethod
    def get(cls, request):
        # Manual authentication check
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get email filter from query parameters
        email = request.GET.get('email', None)
        bookings = Booking.objects.all().order_by('-created_at')

        if email:
            bookings = bookings.filter(
                Q(customer_email__iexact=email) |
                Q(customer_email__icontains=email)
            )

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @classmethod
    def post(cls, request):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            # Use the read serializer for response
            response_serializer = BookingSerializer(booking)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
