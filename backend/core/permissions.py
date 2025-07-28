from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Permite acesso apenas para usuários com role 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'

class IsManager(BasePermission):
    """
    Permite acesso apenas para usuários com role 'manager'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'manager'

class IsAuditor(BasePermission):
    """
    Permite acesso apenas para usuários com role 'auditor'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'auditor'