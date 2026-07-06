from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Certificate
from .serializers import CertificateSerializer


class CertificateListCreateView(generics.ListCreateAPIView):
    """
    Lista los certificados según el usuario autenticado
    y permite crear nuevos certificados desde la API.
    """
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == "admin":
            return Certificate.objects.select_related(
                "enrollment",
                "enrollment__student",
                "enrollment__course"
            ).all()

        return Certificate.objects.select_related(
            "enrollment",
            "enrollment__student",
            "enrollment__course"
        ).filter(
            enrollment__student=user
        )


class CertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un certificado específico
    respetando los permisos del usuario autenticado.
    """
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == "admin":
            return Certificate.objects.select_related(
                "enrollment",
                "enrollment__student",
                "enrollment__course"
            ).all()

        return Certificate.objects.select_related(
            "enrollment",
            "enrollment__student",
            "enrollment__course"
        ).filter(
            enrollment__student=user
        )


@login_required
def my_certificates(request):
    """
    Muestra los certificados del estudiante autenticado.
    """
    certificates = Certificate.objects.select_related(
        "enrollment",
        "enrollment__course"
    ).filter(
        enrollment__student=request.user
    )

    return render(
        request,
        "certificates/list.html",
        {"certificates": certificates}
    )