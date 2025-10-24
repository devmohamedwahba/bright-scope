from django.urls import path

from .views import ContactInfoViewSet

urlpatterns = [
    path('contact-info/', ContactInfoViewSet.as_view({"get": "list"}), name='contact-info'),

]
