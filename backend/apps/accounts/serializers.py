"""Serializers do app accounts (User e perfil, JWT)."""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Dados públicos do usuário (id, username, email, first_name, last_name, date_joined)."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Perfil editável (email, first_name, last_name); demais campos read_only."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
        ]
        read_only_fields = ["id", "username", "date_joined", "is_active"]
