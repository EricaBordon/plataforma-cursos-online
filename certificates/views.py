from rest_framework import generics
from .models import Certificate
from .serializers import CertificateSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class CertificateListCreateView(generics.ListCreateAPIView):
    """
    Lista todos los certificados y permite crear nuevos certificados.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class CertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un certificado específico.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer



@login_required(login_url="/login/")
def my_certificates(request):

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