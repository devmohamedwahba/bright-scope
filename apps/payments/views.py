from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Payment
from .serializers import PaymentCreateSerializer
from .services.paytabs_service import PayTabsService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

class CreatePaymentView(APIView):
    # permission_classes = [permissions.IsAuthenticated]  # Optional: JWT protection

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        paytabs = PayTabsService()
        # base_url = f"{request.scheme}://{request.get_host()}"

        try:
            result = paytabs.create_payment_session(payment)
            tran_ref = result.get("tran_ref")
            payment.transaction_reference = tran_ref
            payment.save()

            return Response({
                "payment_url": result.get("redirect_url"),
                "transaction_reference": tran_ref,
                "status": "INITIATED"
            })
        except Exception as e:
            logger.error(f"PayTabs Error: {e}")
            payment.status = "FAILED"
            payment.save()
            return Response({"error": "Unable to initiate payment."},
                            status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')  # PayTabs callback will come without CSRF token
class PayTabsCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        tran_ref = data.get("tran_ref")
        result = data.get("payment_result", {}).get("response_status")

        if not tran_ref:
            return Response({"error": "Missing transaction reference."}, status=400)

        try:
            payment = Payment.objects.get(transaction_reference=tran_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)

        if result == "A":
            payment.status = "SUCCESS"
        else:
            payment.status = "FAILED"
        payment.save()

        logger.info(f"Payment {payment.order_id} updated to {payment.status}")
        return Response({"message": "Callback processed successfully."})
