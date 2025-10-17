from django.urls import path
from .views import (ServiceListAPIView, ServiceDetailAPIView, BookingCreateAPIView)

urlpatterns = [
    # Services
    path('services/', ServiceListAPIView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    # Bookings
    path('bookings/', BookingCreateAPIView.as_view(), name='booking-list-create'),
]
