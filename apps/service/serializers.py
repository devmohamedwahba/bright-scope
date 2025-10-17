from rest_framework import serializers
from .models import Service, ServiceFeature, Package, Addon, AddonCategory, Booking


class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = ['id', 'name', 'description', 'icon', 'order']


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id', 'name', 'package_type', 'price', 'square_feet',
            'duration', 'description',
            'is_active', 'order'
        ]


class AddonCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddonCategory
        fields = ['id', 'name', 'description', 'order']


class AddonSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Addon
        fields = [
            'id', 'name', 'description', 'price',
            'category', 'category_name', 'is_active', 'order'
        ]


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'service_type', 'description', 'is_active']


class ServiceDetailSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    packages = PackageSerializer(many=True, read_only=True)
    addons = AddonSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'description',
            'hero_title', 'hero_description', 'features',
            'packages', 'addons', 'is_active'
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    addon_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        default=list
    )

    class Meta:
        model = Booking
        fields = [
            'service', 'package', 'addon_ids',
            'customer_name', 'customer_email', 'customer_phone',
            'address', 'booking_date', 'special_requests'
        ]

    def create(self, validated_data):
        # Extract addon_ids first
        addon_ids = validated_data.pop('addon_ids', [])

        # Get the addons objects
        addons = Addon.objects.filter(id__in=addon_ids, is_active=True) if addon_ids else []

        # Calculate total price
        package = validated_data['package']
        total_price = package.price + sum(addon.price for addon in addons)

        # Create booking
        booking = Booking.objects.create(
            **validated_data,
            total_price=total_price
        )

        # Set many-to-many relationship after booking is created
        if addons:
            booking.addons.set(addons)

        return booking

class BookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_type = serializers.CharField(source='service.service_type', read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_price = serializers.DecimalField(source='package.price', read_only=True, max_digits=8, decimal_places=2)
    addons_details = AddonSerializer(source='addons', many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'service', 'service_name', 'service_type',
            'package', 'package_name', 'package_price',
            'addons', 'addons_details', 'customer_name',
            'customer_email', 'customer_phone', 'address',
            'booking_date', 'special_requests', 'total_price',
            'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at', 'total_price']