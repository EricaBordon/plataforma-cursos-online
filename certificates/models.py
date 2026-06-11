import uuid
from django.db import models

from enrollments.models import Enrollment


class Certificate(models.Model):
    """
    Representa el certificado emitido a un estudiante
    luego de completar un curso.
    """

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="certificate",
        verbose_name="Inscripción"
    )

    certificate_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Código del certificado"
    )

    issued_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de emisión"
    )

    pdf_file = models.FileField(
        upload_to="certificates/",
        blank=True,
        null=True,
        verbose_name="Archivo PDF"
    )

    is_valid = models.BooleanField(
        default=True,
        verbose_name="Certificado válido"
    )

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        ordering = ["-issued_at"]

    def __str__(self):
        return f"Certificado {self.certificate_code}"