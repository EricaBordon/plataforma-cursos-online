from django.urls import path
from .views import (
    CertificateListCreateView,
    CertificateDetailView,
    my_certificates,
)

urlpatterns = [
    path("", CertificateListCreateView.as_view(), name="certificate-list-create"),

    path(
        "<int:pk>/",
        CertificateDetailView.as_view(),
        name="certificate-detail"
    ),

    path(
        "my/",
        my_certificates,
        name="my-certificates"
    ),
]