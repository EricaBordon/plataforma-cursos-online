from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enrollment",
        "amount",
        "status",
        "payment_method",
        "transaction_id",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "transaction_id",
        "enrollment__student__username",
        "enrollment__student__email",
        "enrollment__course__title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )