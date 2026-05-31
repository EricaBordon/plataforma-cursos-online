from rest_framework.permissions import BasePermission
from .models import Role


class IsAdmin(BasePermission):
    message = 'Se requiere rol de administrador.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.ADMIN
        )


class IsInstructor(BasePermission):
    message = 'Se requiere rol de instructor.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.INSTRUCTOR
        )


class IsStudent(BasePermission):
    message = 'Se requiere rol de estudiante.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.STUDENT
        )


class IsAdminOrInstructor(BasePermission):
    message = 'Se requiere rol de admin o instructor.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in [Role.ADMIN, Role.INSTRUCTOR]
        )