import uuid

from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone

from enrollments.models import Enrollment
from .generator import generate_certificate


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.pdf_file:
            student_name = self.enrollment.student.get_full_name()

            if not student_name:
                student_name = self.enrollment.student.email

            course_title = self.enrollment.course.title

            instructor = self.enrollment.course.instructor
            instructor_name = instructor.get_full_name()

            if not instructor_name:
                instructor_name = instructor.email

            date = timezone.localtime(self.issued_at).strftime("%d/%m/%Y")

            pdf_buffer = generate_certificate(
                student_name=student_name,
                course_title=course_title,
                instructor_name=instructor_name,
                date=date,
            )

            file_name = f"certificado_{self.certificate_code}.pdf"

            self.pdf_file.save(
                file_name,
                ContentFile(pdf_buffer.getvalue()),
                save=False
            )

            super().save(update_fields=["pdf_file"])