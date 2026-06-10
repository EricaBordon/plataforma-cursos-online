from django.db import models
from django.conf import settings

from .constants import (
    ENROLLMENT_STATUS_CHOICES,
    PROGRESS_NOT_STARTED,
    PROGRESS_IN_PROGRESS,
    PROGRESS_COMPLETED
)


class Enrollment(models.Model):
    """
    Representa la inscripción de un estudiante a un curso.
    """

    # TODO:
    # Reemplazar course_id por FK real cuando exista Course.
    #
    # from courses.models import Course
    #
    # course = models.ForeignKey(
    #     Course,
    #     on_delete=models.CASCADE,
    #     related_name='enrollments'
    # )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course_id = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default="pending"
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ['student', 'course_id']

    def __str__(self):
        return f"{self.student} - Curso {self.course_id}"


class LessonProgress(models.Model):
    """
    Guarda el progreso del estudiante
    en una lección.
    """

    PROGRESS_CHOICES = [
        (PROGRESS_NOT_STARTED, "No iniciado"),
        (PROGRESS_IN_PROGRESS, "En progreso"),
        (PROGRESS_COMPLETED, "Completado"),
    ]

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    # TODO:
    # Reemplazar por FK real a Lesson.
    lesson_id = models.IntegerField()

    progress_status = models.CharField(
        max_length=20,
        choices=PROGRESS_CHOICES,
        default=PROGRESS_NOT_STARTED
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Lección {self.lesson_id}"