from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    SendPasswordResetEmailView,
    UserPasswordResetView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password-email/', SendPasswordResetEmailView.as_view(), name='reset-password-email'),
    path('reset-password/<uidb64>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]
