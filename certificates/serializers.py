from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    enrollment_detail = serializers.StringRelatedField(
        source="enrollment",
        read_only=True
    )

    class Meta:
        model = Certificate
        fields = [
            "id",
            "enrollment",
            "enrollment_detail",
            "certificate_code",
            "issued_at",
            "pdf_file",
            "is_valid",
        ]

        read_only_fields = [
            "certificate_code",
            "issued_at",
        ]