from django.utils import timezone
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from apps.account.serializers import UserRegistrationSerializer, UserLoginSerializer, SendPasswordResetEmailSerializer, \
    UserPasswordResetSerializer
from apps.account.renderers import UserRenderer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def get_tokens_for_user(user):
    """
    Generate JWT tokens for authenticated user with custom claims
    """
    refresh = RefreshToken.for_user(user)

    # Add custom claims
    refresh['email'] = user.email
    refresh['name'] = user.name
    refresh['user_id'] = user.id

    # Access token claims
    refresh.access_token['email'] = user.email
    refresh.access_token['name'] = user.name
    refresh.access_token['user_id'] = user.id

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'access_token_expiration': refresh.access_token['exp'],
        'refresh_token_expiration': refresh['exp'],
    }


class UserRegistrationView(APIView):
    """
    User registration API view with comprehensive error handling
    """
    permission_classes = []  # Allow unauthenticated access

    @classmethod
    def post(cls, request):
        email = request.data.get('email', '').strip().lower()
        try:
            logger.info(f"Registration attempt for email: {email}")

            # Validate required fields
            required_fields = ['email', 'password', 'name', "phone"]
            for field in required_fields:
                if not request.data.get(field):
                    return Response({
                        'error': 'Validation failed',
                        'details': f'{field} is required'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already exists
            User = get_user_model()  # Import this at top: from django.contrib.auth import get_user_model
            if User.objects.filter(email=email).exists():
                logger.warning(f"Registration attempt with existing email: {email}")
                return Response({
                    'error': 'Validation failed',
                    'details': 'User with this email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate and save user
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Generate tokens
            tokens = get_tokens_for_user(user)

            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            # Log successful registration
            logger.info(f"User registered successfully: {user.email} (ID: {user.id})")

            # Prepare response data
            response_data = {
                'message': 'Registration successful',
                'tokens': tokens,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'phone': user.phone
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            logger.warning(f"Registration validation error for {email}: {e.detail}")
            return Response({
                'error': 'Validation failed',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected registration error for {email}: {str(e)}", exc_info=True)
            return Response({
                'error': 'Registration failed',
                'details': 'An unexpected error occurred. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    @classmethod
    def post(cls, request):
        try:
            # Log login attempt (without password)
            email = request.data.get('email', '').strip().lower()
            logger.info(f"Login attempt for email: {email}")

            # Validate input data
            serializer = UserLoginSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Login validation failed for {email}: {serializer.errors}")
                return Response({
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Extract validated data
            validated_data = serializer.validated_data
            email = validated_data.get('email')
            password = validated_data.get('password')

            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    # Update last login
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    # Generate tokens
                    tokens = get_tokens_for_user(user)

                    # Log successful login
                    logger.info(f"User logged in successfully: {email}")

                    # Prepare response data
                    response_data = {
                        'message': 'Login successful',
                        'tokens': tokens,
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'name': user.name,
                            'phone': user.phone,
                            'is_verified': getattr(user, 'is_verified', False)
                        }
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    # User account is inactive
                    logger.warning(f"Login attempt for inactive account: {email}")
                    return Response({
                        'errors': {
                            'non_field_errors': ['Account is inactive. Please contact support.']
                        }
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                # Authentication failed
                logger.warning(f"Failed login attempt for email: {email}")
                return Response({
                    'errors': {
                        'non_field_errors': ['Invalid email or password.']
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected login error for {email}: {str(e)}", exc_info=True)
            return Response({
                'errors': {
                    'non_field_errors': ['An error occurred during login. Please try again.']
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    @classmethod
    def post(cls, request):
        try:
            serializer = SendPasswordResetEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']

            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Don't reveal whether email exists or not for security
                logger.warning(f"Password reset attempt for non-existent email: {email}")
                return Response(
                    {'msg': 'If the email exists, a password reset link has been sent.'},
                    status=status.HTTP_200_OK
                )

            # Generate password reset token
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build reset URL
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            # Send email
            subject = 'Password Reset Request'
            message = f"""
            Hello {user.name},

            You requested a password reset for your account.
            Please click the link below to reset your password:

            {reset_url}

            This link will expire in 72 hours.

            If you didn't request this, please ignore this email.

            Best regards,
            {settings.SITE_NAME}
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            logger.info(f"Password reset email sent to: {email}")

            return Response(
                {'msg': 'Password reset link sent. Please check your email'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error sending password reset email: {str(e)}")
            return Response(
                {'error': 'Failed to send password reset email. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    @classmethod
    def post(cls, request, uidb64, token):
        try:
            serializer = UserPasswordResetSerializer(
                data=request.data,
                context={'uid': uidb64, 'token': token}
            )
            serializer.is_valid(raise_exception=True)

            # Extract validated data
            password = serializer.validated_data['password']

            # Decode uid and get user
            try:
                user_id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=user_id)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                logger.error(f"Invalid uid for password reset: {uidb64}")
                return Response(
                    {'error': 'Invalid reset link'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify token
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                logger.warning(f"Invalid token for password reset: user_id={user_id}")
                return Response(
                    {'error': 'Reset link has expired or is invalid'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set new password
            user.set_password(password)
            user.save()

            # Invalidate used token
            # Note: Simple token generator doesn't have built-in invalidation
            # Consider using django-rest-passwordreset for more robust solution

            logger.info(f"Password reset successful for user: {user.email}")

            return Response(
                {'msg': 'Password reset successfully'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error resetting password: {str(e)}")
            return Response(
                {'error': 'Failed to reset password. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
