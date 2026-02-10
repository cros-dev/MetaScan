"""
Admin para o app accounts.

Configuração genérica do Django Admin para User.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin customizado para User.

    Mantém todas as funcionalidades padrão do Django UserAdmin,
    permitindo personalização futura se necessário.
    """

    pass
