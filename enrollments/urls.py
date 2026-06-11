from django.urls import path
from .views import (
    EnrollmentListCreateView,
    EnrollmentDetailView,
    student_dashboard,
)

urlpatterns = [
    path("", EnrollmentListCreateView.as_view(), name="enrollment-list-create"),
    path("<int:pk>/", EnrollmentDetailView.as_view(), name="enrollment-detail"),
    path("dashboard/", student_dashboard, name="student-dashboard"),
]