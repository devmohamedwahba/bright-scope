from django.core.management.base import BaseCommand
from apps.contact_us.models import ContactMethod, OfficeLocation


class Command(BaseCommand):
    help = 'Load initial contact data'

    def handle(self, *args, **options):
        # Create contact methods
        contact_methods_data = [
            {
                'method_type': 'phone',
                'title': 'Dubai Office',
                'description': 'Speak directly to our Customer Service Team',
                'value': '+971 XXX XXX XXX',
                'action_text': '+971 XXX XXX XXX',
                'order': 1
            },
            {
                'method_type': 'whatsapp',
                'title': 'Instant Response',
                'description': 'Instant Response - Get immediate assistance through our chat',
                'value': '+971 XXX XXX XXX',
                'action_text': 'Chat Now',
                'order': 2
            },
            {
                'method_type': 'email',
                'title': '24/7 Support',
                'description': 'Send us your queries and we\'ll respond promptly',
                'value': 'info@Brightscope.Ao',
                'action_text': 'info@Brightscope.Ao',
                'order': 3
            }
        ]

        for data in contact_methods_data:
            ContactMethod.objects.get_or_create(
                method_type=data['method_type'],
                defaults=data
            )

        # Create office location
        OfficeLocation.objects.get_or_create(
            office_name="Business Bay, Dubai",
            defaults={
                'title': 'Visit Our Office',
                'description': 'Come visit us at our Dubai headquarters for in-person consultations.',
                'office_address': 'United Arab Emirates',
                'working_hours_name': 'Working Hours',
                'working_hours_weekdays': 'Mon-Fri: 8AM-8PM | Sat: 9AM-6PM',
                'is_primary': True
            }
        )



        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial contact data')
        )