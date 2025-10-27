from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Payment
from .serializers import PaymentCreateSerializer
from .services.paytabs_service import PayTabsService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import requests
from django.conf import settings

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


@method_decorator(csrf_exempt, name='dispatch')
class PayTabsCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        logger.info(f"PayTabs callback received: {data}")

        tran_ref = data.get("tran_ref")
        if not tran_ref:
            return Response({"error": "Missing transaction reference."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the transaction with PayTabs
        headers = {
            "Authorization": f"Bearer {settings.PAYTABS_SERVER_KEY}",
            "Content-Type": "application/json",
        }
        verify_resp = requests.post(
            f"{settings.PAYTABS_BASE_URL}/payment/query",
            json={"tran_ref": tran_ref},
            headers=headers
        ).json()

        result = verify_resp.get("payment_result", {}).get("response_status")

        try:
            payment = Payment.objects.get(transaction_reference=tran_ref)
        except Payment.DoesNotExist:
            logger.warning(f"Payment with tran_ref {tran_ref} not found.")
            return Response({"error": "Payment not found."}, status=status.HTTP_200_OK)

        payment.status = "SUCCESS" if result == "A" else "FAILED"
        payment.save()

        logger.info(f"Payment {payment.order_id} updated to {payment.status}")
        return Response({"message": "Callback processed successfully."}, status=status.HTTP_200_OK)