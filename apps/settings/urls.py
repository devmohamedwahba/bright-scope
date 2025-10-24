from django.urls import path

from .views import ContactInfoViewSet

urlpatterns = [
    path('contact-info/', ContactInfoViewSet.as_view(), name='contact-info'),

]
