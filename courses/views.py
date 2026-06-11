from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from enrollments.models import Enrollment
from .models import Course


def home(request):
    """
    Muestra la página principal con los cursos publicados.
    """
    courses = Course.objects.filter(is_published=True)
    return render(request, "courses/home.html", {"courses": courses})


def course_detail(request, pk):
    """
    Muestra el detalle de un curso publicado.
    """

    course = get_object_or_404(
        Course,
        pk=pk,
        is_published=True
    )

    course.price_display = f"{int(course.price):,}".replace(",", ".")

    return render(
        request,
        "courses/course_detail.html",
        {"course": course}
    )


@login_required(login_url="/admin/login/")
def enroll_course(request, pk):
    """
    Permite que un usuario autenticado se inscriba a un curso.
    """
    course = get_object_or_404(Course, pk=pk, is_published=True)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
    )

    if created:
        messages.success(request, "Te inscribiste correctamente al curso.")
    else:
        messages.info(request, "Ya estás inscrito en este curso.")

    return redirect("course-detail-web", pk=course.pk)