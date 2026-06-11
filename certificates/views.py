from rest_framework import generics
from .models import Certificate
from .serializers import CertificateSerializer


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