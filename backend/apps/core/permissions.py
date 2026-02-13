from rest_framework import permissions
from apps.accounts.models import User
from . import messages


class IsAdmin(permissions.BasePermission):
    """Permite acesso apenas a administradores."""

    message = messages.PERMISSION_DENIED

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsManager(permissions.BasePermission):
    """Permite acesso a gestores e administradores."""

    message = messages.PERMISSION_DENIED

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role in [User.Role.MANAGER, User.Role.ADMIN]


class IsAuditor(permissions.BasePermission):
    """Permite acesso a conferentes, gestores e administradores."""

    message = messages.PERMISSION_DENIED

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role in [
            User.Role.AUDITOR,
            User.Role.MANAGER,
            User.Role.ADMIN,
        ]


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite escrita apenas ao dono do objeto (obj.user).
    Leitura (SAFE_METHODS) permitida para todos autenticados.
    """

    message = messages.PERMISSION_DENIED

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
