from rest_framework import serializers
from django.utils import timezone

from .models import Enrollment, LessonProgress


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer para inscripciones.
    """

    class Meta:
        model = Enrollment
        fields = '__all__'


class LessonProgressSerializer(serializers.ModelSerializer):
    """
    Serializer para progreso de lecciones.
    """

    class Meta:
        model = LessonProgress
        fields = '__all__'

    def update(self, instance, validated_data):

        # Si la lección se marca como completada,
        # guardar fecha de finalización.
        if validated_data.get('is_completed'):

            if not instance.is_completed:
                validated_data['completed_at'] = timezone.now()

        return super().update(instance, validated_data)