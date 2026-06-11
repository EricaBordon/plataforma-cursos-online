from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class PaymentListCreateView(generics.ListCreateAPIView):
    """
    Lista todos los pagos y permite registrar nuevos pagos.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un pago específico.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


@login_required(login_url="/login/")
def payment_history(request):
    """
    Historial de pagos del estudiante autenticado.
    """
    payments = Payment.objects.select_related(
        "enrollment",
        "enrollment__course"
    ).filter(
        enrollment__student=request.user
    )

    return render(
        request,
        "payments/history.html",
        {"payments": payments}
    )