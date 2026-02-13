"""Permissões genéricas do app core (reutilizáveis no projeto)."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Apenas o dono pode editar; outros só leitura. Objeto deve ter owner ou user."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "owner"):
            return obj.owner == request.user

        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
