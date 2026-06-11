from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import generics

from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentListCreateView(generics.ListCreateAPIView):
    """
    Lista todas las inscripciones y permite crear nuevas.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina una inscripción específica.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


@login_required(login_url="/admin/login/")
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