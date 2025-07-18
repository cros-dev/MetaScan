from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrOwnerBase(BasePermission):
    """
    Permite acesso total para staff. Usuário comum só pode acessar objetos que ele 'possui'.
    POST só para staff. Leitura para autenticados.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_staff
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return self.is_owner(request, obj)

    def is_owner(self, request, obj):
        raise NotImplementedError("Subclasses devem implementar is_owner.")

class IsStaffOrCavaleteUser(IsStaffOrOwnerBase):
    def is_owner(self, request, obj):
        return obj.user == request.user

class IsStaffOrSlotUser(IsStaffOrOwnerBase):
    def is_owner(self, request, obj):
        return obj.cavalete and obj.cavalete.user == request.user

class IsStaffOrHistoricoUser(IsStaffOrOwnerBase):
    def is_owner(self, request, obj):
        return obj.user == request.user