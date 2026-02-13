"""Admin do app accounts (User customizado)."""

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

    Adiciona o campo 'role' à listagem e aos fieldsets.
    """

    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    fieldsets = BaseUserAdmin.fieldsets + (("MetaScan Info", {"fields": ("role",)}),)

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("MetaScan Info", {"fields": ("role",)}),
    )
