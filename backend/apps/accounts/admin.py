"""Admin do app accounts (User customizado)."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """UserAdmin customizado (base Django, personalizável)."""

    pass
