from django.conf import settings
from django.db import models

from courses.models import Course
from .constants import (
    ENROLLMENT_STATUS_CHOICES,
    PROGRESS_NOT_STARTED,
    PROGRESS_IN_PROGRESS,
    PROGRESS_COMPLETED,
)


class Enrollment(models.Model):
    """
    Representa la inscripción de un estudiante a un curso.
    """

    PROGRESS_CHOICES = [
        (PROGRESS_NOT_STARTED, "No iniciado"),
        (PROGRESS_IN_PROGRESS, "En progreso"),
        (PROGRESS_COMPLETED, "Completado"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Estudiante"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Curso"
    )

    status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default="pending",
        verbose_name="Estado de inscripción"
    )

    progress_status = models.CharField(
        max_length=20,
        choices=PROGRESS_CHOICES,
        default=PROGRESS_NOT_STARTED,
        verbose_name="Estado del progreso"
    )

    progress_percentage = models.PositiveIntegerField(
        default=0,
        verbose_name="Porcentaje de progreso"
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de inscripción"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ("student", "course")
        ordering = ["-enrolled_at"]

    def __str__(self):
        return f"{self.student} - {self.course}"

    def mark_as_completed(self):
        """
        Marca la inscripción como completada.
        """
        self.progress_status = PROGRESS_COMPLETED
        self.progress_percentage = 100
        self.save()