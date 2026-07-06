from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses.models import Lesson

from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer


class EnrollmentListCreateView(generics.ListCreateAPIView):
    """
    Lista las inscripciones según el usuario autenticado
    y permite crear nuevas inscripciones desde la API.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == "admin":
            return Enrollment.objects.select_related(
                "student",
                "course"
            ).all()

        return Enrollment.objects.select_related(
            "student",
            "course"
        ).filter(
            student=user
        )


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina una inscripción específica
    respetando los permisos del usuario autenticado.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == "admin":
            return Enrollment.objects.select_related(
                "student",
                "course"
            ).all()

        return Enrollment.objects.select_related(
            "student",
            "course"
        ).filter(
            student=user
        )


@login_required
def student_dashboard(request):
    """
    Muestra los cursos inscritos del estudiante autenticado.
    """
    enrollments = request.user.enrollments.select_related("course").all()

    return render(
        request,
        "enrollments/dashboard.html",
        {"enrollments": enrollments}
    )


@login_required
def mark_lesson_completed(request, lesson_id):
    """
    Marca una lección como completada para el estudiante autenticado.
    Actualiza el porcentaje de progreso de la inscripción.
    Si completa todas las lecciones, marca el curso como completado
    y genera certificado.
    """

    lesson = get_object_or_404(
        Lesson,
        pk=lesson_id
    )

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=lesson.module.course,
        status="paid"
    )

    lesson_progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    if not lesson_progress.is_completed:
        lesson_progress.is_completed = True
        lesson_progress.completed_at = timezone.now()
        lesson_progress.save()

        messages.success(
            request,
            "Lección marcada como completada."
        )
    else:
        messages.info(
            request,
            "Esta lección ya estaba completada."
        )

    total_lessons = Lesson.objects.filter(
        module__course=enrollment.course
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        enrollment=enrollment,
        is_completed=True
    ).count()

    if total_lessons > 0:
        enrollment.progress_percentage = int(
            (completed_lessons / total_lessons) * 100
        )
    else:
        enrollment.progress_percentage = 0

    if enrollment.progress_percentage >= 100:
        enrollment.progress_status = "completed"

       

        messages.success(
            request,
            "¡Felicitaciones! Completaste todas las lecciones. Ya puedes rendir el examen final para obtener tu certificado."
        )

    elif enrollment.progress_percentage > 0:
        enrollment.progress_status = "in_progress"

    else:
        enrollment.progress_status = "not_started"

    enrollment.save()

    return redirect(
        "course-detail-web",
        pk=enrollment.course.pk
    )