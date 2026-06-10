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