from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  ContactMethod, OfficeLocation
from .serializers import (
    ContactSubmissionSerializer,
    ContactMethodSerializer,
    OfficeLocationSerializer,ContactInfoSerializer
)

class ContactSubmissionCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactSubmissionSerializer(data=request.data)

        if serializer.is_valid():
            # Save the contact submission
            contact_submission = serializer.save()

            return Response({
                'message': 'Thank you for your submission. We will get back to you within 24 hours.',
                'data': ContactSubmissionSerializer(contact_submission).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': 'Please correct the errors below.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ContactInfoView(APIView):
    def get(self, request):
        # Get active contact methods
        contact_methods = ContactMethod.objects.filter(is_active=True)
        # Get office locations
        office_locations = OfficeLocation.objects.all()

        data = {
            "contact_methods": contact_methods,
            "office_locations": office_locations,
        }

        serializer = ContactInfoSerializer(data, context={'request': request})
        return Response(serializer.data)