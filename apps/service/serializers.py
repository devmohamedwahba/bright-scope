from rest_framework import serializers
from .models import Service, ServiceFeature, Package, Addon, AddonCategory, Booking, ServiceContent, ServiceRating

class ServiceFeatureSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ServiceFeature
        fields = ['id', 'name', 'description', 'icon', 'order']

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class ServiceContentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ServiceContent
        fields = ['id', 'name', 'order']

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class ServiceRatingSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRating
        fields = ['id', 'name', 'description', 'icon', 'order']

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class PackageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    square_feet = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'package_type', 'price',
            'square_feet', 'duration', 'description',
            'is_active', 'order'
        ]

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def get_square_feet(self, obj):
        language = self._get_language()
        return obj.square_feet_ar if language == 'ar' and obj.square_feet_ar else obj.square_feet

    def get_duration(self, obj):
        language = self._get_language()
        return obj.duration_ar if language == 'ar' and obj.duration_ar else obj.duration

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class AddonCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = AddonCategory
        fields = ['id', 'name', 'description', 'is_active', 'order']

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class AddonSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Addon
        fields = [
            'id', 'name', 'description', 'category',
            'category_name', 'price', 'is_active', 'order'
        ]

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class ServiceListSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    contents = ServiceContentSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    hero_title = serializers.SerializerMethodField()
    sub_hero_title = serializers.SerializerMethodField()
    hero_description = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'start_price', 'service_type', 'description', 'icon',
            'is_active', 'hero_title', 'sub_hero_title', 'hero_description',
            'image_url', 'features', 'contents'
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def get_hero_title(self, obj):
        language = self._get_language()
        return obj.hero_title_ar if language == 'ar' and obj.hero_title_ar else obj.hero_title

    def get_sub_hero_title(self, obj):
        language = self._get_language()
        return obj.sub_hero_title_ar if language == 'ar' and obj.sub_hero_title_ar else obj.sub_hero_title

    def get_hero_description(self, obj):
        language = self._get_language()
        return obj.hero_description_ar if language == 'ar' and obj.hero_description_ar else obj.hero_description

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'


class ServiceDetailSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    contents = ServiceContentSerializer(many=True, read_only=True)
    ratings = ServiceRatingSerializer(many=True, read_only=True)
    packages = PackageSerializer(many=True, read_only=True)
    addons = AddonSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    hero_title = serializers.SerializerMethodField()
    sub_hero_title = serializers.SerializerMethodField()
    hero_description = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'start_price', 'service_type',
            'description', 'icon', 'is_active', 'hero_title',
            'sub_hero_title', 'hero_description', 'image',
            'image_url', 'features', 'contents', 'ratings',
            'packages', 'addons', 'created_at', 'updated_at'
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_name(self, obj):
        language = self._get_language()
        return obj.name_ar if language == 'ar' and obj.name_ar else obj.name

    def get_description(self, obj):
        language = self._get_language()
        return obj.description_ar if language == 'ar' and obj.description_ar else obj.description

    def get_hero_title(self, obj):
        language = self._get_language()
        return obj.hero_title_ar if language == 'ar' and obj.hero_title_ar else obj.hero_title

    def get_sub_hero_title(self, obj):
        language = self._get_language()
        return obj.sub_hero_title_ar if language == 'ar' and obj.sub_hero_title_ar else obj.sub_hero_title

    def get_hero_description(self, obj):
        language = self._get_language()
        return obj.hero_description_ar if language == 'ar' and obj.hero_description_ar else obj.hero_description

    def _get_language(self):
        request = self.context.get('request')
        if request:
            lang = request.query_params.get('lang', '').lower()
            if lang in ['ar', 'en']:
                return lang
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if 'ar' in accept_language.lower():
                return 'ar'
        return 'en'

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