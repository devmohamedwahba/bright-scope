from django.urls import path
from .views import CreatePaymentView, PayTabsCallbackView

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create-payment"),
    path("callback/", PayTabsCallbackView.as_view(), name="paytabs-callback"),
]
