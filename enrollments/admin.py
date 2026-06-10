from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "course",
        "status",
        "progress_status",
        "progress_percentage",
        "enrolled_at",
    )

    list_filter = (
        "status",
        "progress_status",
        "enrolled_at",
    )

    search_fields = (
        "student__username",
        "student__email",
        "course__title",
    )

    readonly_fields = (
        "enrolled_at",
        "updated_at",
    )