from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from enrollments.models import Enrollment

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


@login_required(login_url="/admin/login/")
def simulate_payment(request, enrollment_id):
    """
    Simula un pago exitoso para pruebas.
    """

    enrollment = get_object_or_404(
        Enrollment,
        pk=enrollment_id,
        student=request.user
    )

    payment, created = Payment.objects.get_or_create(
        enrollment=enrollment,
        defaults={
            "amount": enrollment.course.price,
            "status": "approved",
            "transaction_id": f"TEST-{enrollment.id}",
            "paid_at": timezone.now(),
        }
    )

    if not created:

        payment.status = "approved"
        payment.paid_at = timezone.now()

        payment.save()

    enrollment.status = "paid"
    enrollment.save()

    messages.success(
        request,
        "Pago realizado correctamente."
    )

    return redirect(
        "course-detail-web",
        pk=enrollment.course.id
    )