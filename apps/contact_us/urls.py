from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.ContactSubmissionCreateView.as_view(), name='contact-submit'),
    path('info/', views.ContactInfoView.as_view(), name='contact-info')
]