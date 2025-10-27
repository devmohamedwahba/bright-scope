from django.urls import path
from .views import CreatePaymentView, PayTabsCallbackView, PayTabsReturnView

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create-payment"),
    path("callback/", PayTabsCallbackView.as_view(), name="paytabs-callback"),
    path("return/", PayTabsReturnView.as_view(), name="paytabs-return"),
]
