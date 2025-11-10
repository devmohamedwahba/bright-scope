from rest_framework import serializers
from .models import ContactSubmission, ContactMethod, OfficeLocation
from django.core.validators import RegexValidator
import re
from django.utils import timezone


class ContactSubmissionSerializer(serializers.ModelSerializer):
    # Custom field-level validation
    full_name = serializers.CharField(
        max_length=200,
        min_length=2,
        error_messages={
            'required': 'Full name is required',
            'blank': 'Full name cannot be blank',
            'min_length': 'Full name must be at least 2 characters long',
            'max_length': 'Full name cannot exceed 200 characters'
        }
    )

    email = serializers.EmailField(
        error_messages={
            'required': 'Email address is required',
            'invalid': 'Please enter a valid email address'
        }
    )

    phone_number = serializers.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+971XXXXXXXXX'. Up to 15 digits allowed."
            )
        ]
    )

    message = serializers.CharField(
        min_length=10,
        max_length=1000,
        error_messages={
            'required': 'Message is required',
            'min_length': 'Message must be at least 10 characters long',
            'max_length': 'Message cannot exceed 1000 characters'
        }
    )

    class Meta:
        model = ContactSubmission
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_resolved')

    def validate_full_name(self, value):
        """
        Validate full name contains only letters, spaces, and basic punctuation
        """
        # Remove extra spaces
        value = ' '.join(value.split())

        # Check if name contains only allowed characters
        if not re.match(r'^[a-zA-Z\s\.\-\']+$', value):
            raise serializers.ValidationError(
                "Name can only contain letters, spaces, hyphens, apostrophes, and periods"
            )

        # Check if name has at least first and last name
        name_parts = value.split()
        if len(name_parts) < 2:
            raise serializers.ValidationError(
                "Please enter your full name (first and last name)"
            )

        # Capitalize properly
        value = value.title()

        return value

    # def validate_phone_number(self, value):
    #     """
    #     Enhanced phone number validation for UAE numbers
    #     """
    #     # Clean the phone number
    #     value = value.strip().replace(' ', '').replace('-', '')
    #
    #     # Check if it starts with UAE country code
    #     if not value.startswith('+971'):
    #         # If it doesn't start with +971, try to add it
    #         if value.startswith('971'):
    #             value = '+' + value
    #         elif value.startswith('0'):
    #             value = '+971' + value[1:]
    #         else:
    #             value = '+971' + value
    #
    #     # Validate UAE phone number format
    #     uae_phone_pattern = r'^\+971(?:[2-9]\d{7}|5[024568]\d{7})$'
    #     if not re.match(uae_phone_pattern, value):
    #         raise serializers.ValidationError(
    #             "Please enter a valid UAE phone number (e.g., +971501234567)"
    #         )
    #
    #     return value

    def validate_email(self, value):
        """
        Enhanced email validation
        """
        value = value.strip().lower()

        # Check for disposable email domains
        disposable_domains = [
            'tempmail.com', 'throwaway.com', 'fake.com', 'guerrillamail.com',
            'mailinator.com', 'yopmail.com', 'temp-mail.org'
        ]

        domain = value.split('@')[-1]
        if domain in disposable_domains:
            raise serializers.ValidationError(
                "Disposable email addresses are not allowed"
            )

        return value

    def validate_service_type(self, value):
        """
        Validate service type is one of the available choices
        """
        valid_types = dict(ContactSubmission.SERVICE_TYPES)
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid service type. Must be one of: {', '.join(valid_types.keys())}"
            )
        return value

    def validate_message(self, value):
        """
        Validate message content
        """
        value = value.strip()

        # Check minimum length after stripping
        if len(value) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long"
            )

        # Check for excessive capitalization (potential spam)
        if value.isupper():
            raise serializers.ValidationError(
                "Please avoid writing entire message in uppercase"
            )

        # Check for excessive repetition (potential spam)
        words = value.split()
        if len(words) > 5 and len(set(words)) < len(words) * 0.3:
            raise serializers.ValidationError(
                "Message appears to contain excessive repetition"
            )

        return value

    def validate(self, data):
        """
        Object-level validation
        """
        # Check for duplicate submissions (same email and similar message)
        if self.instance is None:  # Only for new submissions
            recent_duplicate = ContactSubmission.objects.filter(
                email=data['email'],
                message__icontains=data['message'][:50],  # Check first 50 chars
                created_at__gte=timezone.now() - timezone.timedelta(hours=24)
            ).exists()

            if recent_duplicate:
                raise serializers.ValidationError({
                    'message': 'You have already submitted a similar message recently. Please wait 24 hours before submitting again.'
                })

        # Validate that message is not just repeating the name
        if data['full_name'].lower() in data['message'].lower():
            name_words = data['full_name'].lower().split()
            message_words = data['message'].lower().split()

            # If message is too similar to name
            if len(set(name_words) & set(message_words)) / len(name_words) > 0.7:
                raise serializers.ValidationError({
                    'message': 'Message should provide more details about your inquiry'
                })

        return data

    def create(self, validated_data):
        """
        Custom create method to add additional processing
        """
        # You can add additional processing here if needed
        instance = super().create(validated_data)

        # Log the submission (optional)
        print(f"New contact submission from {validated_data['email']}")

        return instance


class ContactMethodSerializer(serializers.ModelSerializer):
    title_display = serializers.SerializerMethodField()
    description_display = serializers.SerializerMethodField()
    action_text_display = serializers.SerializerMethodField()

    class Meta:
        model = ContactMethod
        fields = [
            'id',
            'icon',
            'method_type',
            'title_display',
            'description_display',
            'value',
            'action_text_display',
            'is_active',
            'order'
        ]

    def get_title_display(self, obj):
        language = self._get_language()
        return obj.title_ar if language == 'ar' and obj.title_ar else obj.title

    def get_description_display(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def get_action_text_display(self, obj):
        language = self._get_language()
        if language == 'ar' and obj.action_text_ar:
            return obj.action_text_ar
        return obj.action_text or ""

    def _get_language(self):
        """Extract language from request query parameters or headers"""
        request = self.context.get('request')
        if request:
            # Check query parameter first
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang

            # Check Accept-Language header
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'

        return 'en'  # Default to English

class OfficeLocationSerializer(serializers.ModelSerializer):
    title_display = serializers.SerializerMethodField()
    description_display = serializers.SerializerMethodField()
    office_name_display = serializers.SerializerMethodField()
    office_address_display = serializers.SerializerMethodField()
    working_hours_name_display = serializers.SerializerMethodField()
    working_hours_weekdays_display = serializers.SerializerMethodField()
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = OfficeLocation
        fields = [
            'id',
            'icon',
            'title_display',
            'description_display',
            'office_name_display',
            'office_address_display',
            'working_hours_name_display',
            'working_hours_weekdays_display',
            'full_address',
            'google_maps_link',
            'is_primary'
        ]

    def get_title_display(self, obj):
        language = self._get_language()
        return obj.title_ar if language == 'ar' and obj.title_ar else obj.title

    def get_description_display(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def get_office_name_display(self, obj):
        language = self._get_language()
        return obj.office_name_ar if language == 'ar' and obj.office_name_ar else obj.office_name

    def get_office_address_display(self, obj):
        language = self._get_language()
        return obj.office_address_ar if language == 'ar' and obj.office_address_ar else obj.office_address

    def get_working_hours_name_display(self, obj):
        language = self._get_language()
        return obj.working_hours_name_ar if language == 'ar' and obj.working_hours_name_ar else obj.working_hours_name

    def get_working_hours_weekdays_display(self, obj):
        language = self._get_language()
        return obj.working_hours_weekdays_ar if language == 'ar' and obj.working_hours_weekdays_ar else obj.working_hours_weekdays

    def get_full_address(self, obj):
        language = self._get_language()
        if language == 'ar':
            return f"{obj.office_name_ar}, {obj.office_address_ar}"
        else:
            return f"{obj.office_name}, {obj.office_address}"

    def _get_language(self):
        """Extract language from request query parameters or headers"""
        request = self.context.get('request')
        if request:
            # Check query parameter first
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang

            # Check Accept-Language header
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'

        return 'en'  # Default to English

class ContactInfoSerializer(serializers.Serializer):
    contact_methods = ContactMethodSerializer(many=True, read_only=True)
    office_locations = OfficeLocationSerializer(many=True, read_only=True)
    current_language = serializers.SerializerMethodField()

    def get_current_language(self, obj):
        """Get language from the serializer context"""
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang

            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'

        return 'en'

    def to_representation(self, instance):
        """Override to properly structure the data"""
        # Since we're using this as a wrapper serializer,
        # we need to build the representation manually
        return {
            'contact_methods': ContactMethodSerializer(
                instance['contact_methods'],
                many=True,
                context=self.context
            ).data,
            'office_locations': OfficeLocationSerializer(
                instance['office_locations'],
                many=True,
                context=self.context
            ).data,
            'current_language': self.get_current_language(instance)
        }