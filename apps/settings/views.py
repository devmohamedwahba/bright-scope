from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ContactInfo
from .serializers import ContactInfoSerializer, NewsletterSubscriberSerializer


class ContactInfoViewSet(viewsets.ViewSet):
    """
    ViewSet for contact information with multilingual support
    """

    def list(self, request):
        """
        Get contact information
        Supports language parameter: ?lang=en or ?lang=ar
        Also supports Accept-Language header
        """
        try:
            # Try to get existing contact info
            contact_info = ContactInfo.objects.first()

            # If none exists, create default one
            if not contact_info:
                contact_info = ContactInfo.objects.create()

            serializer = ContactInfoSerializer(contact_info, context={'request': request})
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Failed to retrieve contact information"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """
        Newsletter subscription endpoint
        """
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            try:
                subscriber = serializer.save()
                return Response(
                    {
                        "message": "Successfully subscribed to newsletter!",
                        "email": subscriber.email
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to subscribe. Please try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
