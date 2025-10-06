from rest_framework import serializers
from apps.account.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=8,
        help_text="Enter the same password as above for verification"
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {'input_type': 'password'},
                'help_text': "Password must be at least 8 characters long"
            },
            'email': {
                'required': True,
                'help_text': "Enter a valid email address"
            },
            'name': {
                'required': True,
                'help_text': "Enter your full name"
            },
            'phone': {
                'required': True,
                'help_text': "Enter UAE phone number (e.g., +9715XXXXXXXX, 05XXXXXXXX, 9715XXXXXXXX)"
            }
        }

    @classmethod
    def validate_password(cls, value):
        """
        Validate password using Django's built-in password validators
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    @classmethod
    def validate_email(cls, value):
        """
        Check if email already exists
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    @classmethod
    def validate_phone(cls, value):
        """
        UAE phone number validation
        """
        # Remove any spaces, dashes, or other characters
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', value)

        # UAE phone number patterns
        uae_patterns = [
            r'^9715\d{8}$',  # +9715XXXXXXXX
            r'^05\d{8}$',  # 05XXXXXXXX
            r'^5\d{8}$',  # 5XXXXXXXX (without country code)
            r'^009715\d{8}$',  # 009715XXXXXXXX
        ]

        # Check if the phone number matches any UAE pattern
        is_valid = any(re.match(pattern, clean_phone) for pattern in uae_patterns)

        if not is_valid:
            raise serializers.ValidationError(
                "Please enter a valid UAE phone number. "
                "Formats: +9715XXXXXXXX, 05XXXXXXXX, 5XXXXXXXX, or 009715XXXXXXXX"
            )

        # Normalize to international format (+9715XXXXXXXX)
        if clean_phone.startswith('05'):
            clean_phone = '971' + clean_phone[1:]  # 05XXXXXXXX -> 9715XXXXXXXX
        elif clean_phone.startswith('5') and len(clean_phone) == 9:
            clean_phone = '971' + clean_phone  # 5XXXXXXXX -> 9715XXXXXXXX
        elif clean_phone.startswith('00971'):
            clean_phone = '971' + clean_phone[5:]  # 009715XXXXXXXX -> 9715XXXXXXXX

        # Ensure it starts with + for international format
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone

        # Check if phone number already exists
        if User.objects.filter(phone=clean_phone).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")

        return clean_phone

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({
                "password2": "Password and Confirm Password don't match."
            })

        # Remove password2 from attributes as it's not needed for user creation
        attrs.pop('password2')
        return attrs

    def create(self, validated_data):
        """
        Create user with hashed password
        """
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    @classmethod
    def validate_email(cls, value):
        """
        Validate and normalize email
        """
        value = value.strip().lower()

        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Please enter a valid email address.")

        return value

    def validate(self, attrs):
        """
        Additional validation if needed
        """
        email = attrs.get('email')
        password = attrs.get('password')

        # Add any additional validation logic here
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate_password(self, value):
        """
        Validate password strength
        """
        # Basic validation instead of full Django validation if you prefer
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        if value.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric.")

        if value.isalpha():
            raise serializers.ValidationError("Password must contain at least one number.")

        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": "Passwords don't match."
            })

        return attrs
