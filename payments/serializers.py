from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    enrollment_detail = serializers.StringRelatedField(
        source="enrollment",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "enrollment",
            "enrollment_detail",
            "amount",
            "status",
            "payment_method",
            "transaction_id",
            "paid_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El monto del pago debe ser mayor a cero."
            )
        return value