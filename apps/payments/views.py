from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Payment
from .serializers import PaymentCreateSerializer
from .services.paytabs_service import PayTabsService
import logging
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


class CreatePaymentView(APIView):

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        paytabs = PayTabsService()

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

        paytabs = PayTabsService()
        result = paytabs.verify_payment(tran_ref)

        try:
            payment = Payment.objects.get(transaction_reference=tran_ref)
        except Payment.DoesNotExist:
            logger.warning(f"Payment with tran_ref {tran_ref} not found.")
            return Response({"error": "Payment not found."}, status=status.HTTP_200_OK)

        status_code = result.get("payment_result", {}).get("response_status")
        payment.status = "SUCCESS" if status_code == "A" else "FAILED"
        payment.save()

        logger.info(f"Payment {payment.order_id} updated to {payment.status}")
        return Response({"message": "Callback processed successfully."}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PayTabsReturnView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Handle browser GET redirect."""
        data = request.query_params
        return self.handle_payment_result(data)

    def post(self, request):
        """Handle POST redirect (PayTabs sends JSON or form data)."""
        data = request.data
        return self.handle_payment_result(data)

    def handle_payment_result(self, data):
        """Common handler for both GET and POST."""
        tran_ref = data.get("tranRef") or data.get("tran_ref")
        if not tran_ref:
            return Response({"error": "Missing tran_ref"}, status=400)

        paytabs = PayTabsService()
        result = paytabs.verify_payment(tran_ref)
        logger.info(f"PayTabs return verification for {tran_ref}: {result}")

        payment_status = result.get("payment_result", {}).get("response_status", "")
        frontend_base_url = "https://bright-scope.vercel.app"

        if payment_status in ["A", "success", "APPROVED"]:
            redirect_url = f"{frontend_base_url}/payment-success?tranRef={tran_ref}"
        else:
            redirect_url = f"{frontend_base_url}/payment-failed?tranRef={tran_ref}"

        return HttpResponseRedirect(redirect_url)