from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Enrollment, LessonProgress
from .serializers import (
    EnrollmentSerializer,
    LessonProgressSerializer
)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    CRUD de inscripciones.
    """

    queryset = Enrollment.objects.all()

    serializer_class = EnrollmentSerializer

    permission_classes = [IsAuthenticated]


class LessonProgressViewSet(viewsets.ModelViewSet):
    """
    CRUD de progreso de lecciones.
    """

    queryset = LessonProgress.objects.all()

    serializer_class = LessonProgressSerializer

    permission_classes = [IsAuthenticated]