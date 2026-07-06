from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from enrollments.models import Enrollment
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    """
    Lista los pagos según el usuario autenticado
    y permite registrar nuevos pagos desde la API.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == "admin":
            return Payment.objects.select_related(
                "enrollment",
                "enrollment__student",
                "enrollment__course"
            ).all()

        return Payment.objects.select_related(
            "enrollment",
            "enrollment__student",
            "enrollment__course"
        ).filter(
            enrollment__student=user
        )


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un pago específico
    respetando los permisos del usuario autenticado.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == "admin":
            return Payment.objects.select_related(
                "enrollment",
                "enrollment__student",
                "enrollment__course"
            ).all()

        return Payment.objects.select_related(
            "enrollment",
            "enrollment__student",
            "enrollment__course"
        ).filter(
            enrollment__student=user
        )


@login_required
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


@login_required
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
        payment.amount = enrollment.course.price
        payment.status = "approved"
        payment.transaction_id = payment.transaction_id or f"TEST-{enrollment.id}"
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