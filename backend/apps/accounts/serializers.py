"""
Serializers para o app accounts.

Serializers genéricos para User do Django, compatíveis com JWT.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para dados públicos do usuário.

    Campos: id, username, email, first_name, last_name, role, date_joined
    Campos somente leitura: id, role, date_joined
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "date_joined"]
        read_only_fields = ["id", "role", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil editável do usuário.

    Campos: id, username, email, first_name, last_name, role, date_joined, is_active
    Campos editáveis: email, first_name, last_name
    Campos somente leitura: id, username, role, date_joined, is_active
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "date_joined",
            "is_active",
        ]
        read_only_fields = ["id", "username", "role", "date_joined", "is_active"]
