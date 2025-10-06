from rest_framework import serializers
from .models import ContactInfo, NewsletterSubscriber


class ContactInfoSerializer(serializers.ModelSerializer):
    working_hours = serializers.SerializerMethodField()

    # services = serializers.SerializerMethodField()
    # quick_links = serializers.SerializerMethodField()

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

    # def get_services(self, obj):
    #     return [
    #         "Home Cleaning",
    #         "Deep Cleaning",
    #         "Pest Control",
    #         "Post-Construction",
    #         "Office & Commercial"
    #     ]
    #
    # def get_quick_links(self, obj):
    #     return [
    #         {"title": "About Us", "url": "/about-us"},
    #         {"title": "Careers", "url": "/careers"},
    #         {"title": "Get Quote", "url": "/get-quote"},
    #         {"title": "Privacy Policy", "url": "/privacy-policy"},
    #         {"title": "Terms of Service", "url": "/terms-of-service"}
    #     ]


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
