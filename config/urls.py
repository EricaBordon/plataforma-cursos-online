from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Usuarios y autenticación JWT
    path("api/users/", include("users.urls")),

    # Inscripciones
    path("api/enrollments/", include("enrollments.urls")),

    #pagos
    path("api/payments/", include("payments.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)