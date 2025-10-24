from rest_framework import serializers
from .models import ContactInfo, NewsletterSubscriber


class ContactInfoSerializer(serializers.ModelSerializer):
    working_hours = serializers.SerializerMethodField()

    class Meta:
        model = ContactInfo
        fields = '__all__'

    @classmethod
    def get_working_hours(cls, obj):
        return {
            'monday_friday': obj.mon_fri_hours,
            'saturday': obj.saturday_hours,
            'sunday': obj.sunday_hours
        }


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
