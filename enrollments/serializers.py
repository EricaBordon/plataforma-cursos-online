from rest_framework import serializers
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.StringRelatedField(source="student", read_only=True)
    course_name = serializers.StringRelatedField(source="course", read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_name",
            "status",
            "progress_status",
            "progress_percentage",
            "enrolled_at",
            "updated_at",
        ]
        read_only_fields = ["enrolled_at", "updated_at"]

    def validate_progress_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "El porcentaje de progreso debe estar entre 0 y 100."
            )
        return value