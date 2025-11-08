from rest_framework import serializers
from .models import ContactInfo, NewsletterSubscriber

from rest_framework import serializers


class ContactInfoSerializer(serializers.ModelSerializer):
    working_hours = serializers.SerializerMethodField()
    address_full = serializers.SerializerMethodField()

    class Meta:
        model = ContactInfo
        fields = [
            'id',
            'company_name',
            'tagline',
            'phone_number',
            'whatsapp_number',
            'address',
            'address_full',
            'building',
            'office',
            'working_hours',
            'emergency_available',
            'facebook_url',
            'instagram_url',
            'linkedin_url',
            'twitter_url',
            'youtube_url',
            'copyright_text',
            'created_at',
            'updated_at'
        ]

    def get_working_hours(self, obj):
        language = self._get_language()

        if language == 'ar':
            return {
                'monday_friday': obj.mon_fri_hours_ar,
                'saturday': obj.saturday_hours_ar,
                'sunday': obj.sunday_hours_ar
            }
        else:
            return {
                'monday_friday': obj.mon_fri_hours,
                'saturday': obj.saturday_hours,
                'sunday': obj.sunday_hours
            }

    def get_address_full(self, obj):
        language = self._get_language()

        if language == 'ar':
            return f"{obj.address_ar}, {obj.building_ar}, {obj.office_ar}"
        else:
            return f"{obj.address}, {obj.building}, {obj.office}"

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        language = self._get_language()

        if language == 'ar':
            # Replace all English text fields with Arabic equivalents
            arabic_fields = {
                'company_name': instance.company_name_ar,
                'tagline': instance.tagline_ar,
                'address': instance.address_ar,
                'building': instance.building_ar,
                'office': instance.office_ar,
                'copyright_text': instance.copyright_text_ar,
            }
            data.update(arabic_fields)

        return data

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    def create(self, validated_data):
        email = validated_data.get('email')
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email
        )
        return subscriber
