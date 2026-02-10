"""
Permissões genéricas para o app core.

Permissões customizadas reutilizáveis em todo o projeto.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada: apenas o dono do objeto pode editá-lo.
    Outros usuários podem apenas ler.

    Requer que o objeto tenha um atributo 'owner' ou 'user'.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "owner"):
            return obj.owner == request.user

        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
