from django.db import models

from enrollments.models import Enrollment
from .constants import (
    PAYMENT_STATUS_CHOICES,
    PAYMENT_STATUS_PENDING,
    PAYMENT_METHOD_CHOICES,
    PAYMENT_METHOD_MERCADOPAGO,
)


class Payment(models.Model):
    """
    Representa el pago realizado por una inscripción.
    """

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Inscripción"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto"
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING,
        verbose_name="Estado del pago"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_MERCADOPAGO,
        verbose_name="Método de pago"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID de transacción"
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de pago"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Pago {self.id} - {self.enrollment} - {self.status}"