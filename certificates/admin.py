from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enrollment",
        "certificate_code",
        "issued_at",
        "is_valid",
    )

    list_filter = (
        "is_valid",
        "issued_at",
    )

    search_fields = (
        "certificate_code",
        "enrollment__student__username",
        "enrollment__student__email",
        "enrollment__course__title",
    )

    readonly_fields = (
        "certificate_code",
        "issued_at",
    )