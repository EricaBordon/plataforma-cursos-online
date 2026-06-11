from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer


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