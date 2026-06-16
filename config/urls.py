from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from enrollments.views import student_dashboard

urlpatterns = [
    # Usuarios web (login, logout, register) - debe ir primero
    path("", include("users.web_urls")),

    path("admin/", admin.site.urls),

    # Usuarios y autenticación JWT
    path("api/users/", include("users.urls")),

    # Inscripciones
    path("api/enrollments/", include("enrollments.urls")),

    #pagos
    path("api/payments/", include("payments.urls")),

    #certificados
    path("api/certificates/", include("certificates.urls")),

    #cursos 
    path("", include("courses.urls")),

    path("dashboard/", student_dashboard, name="student-dashboard"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)