"""Testes dos serializers do app accounts."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserSerializerTestCase(TestCase):
    """Testes para UserSerializer."""

    def setUp(self):
        """Configuração inicial."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_user_serializer_fields(self):
        """Testa se o serializer retorna os campos corretos."""
        serializer = UserSerializer(self.user)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertIn("email", data)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)
        self.assertIn("date_joined", data)

    def test_user_serializer_read_only_fields(self):
        """Testa se campos somente leitura não podem ser editados."""
        serializer = UserSerializer(
            self.user,
            data={"id": 999, "username": "newuser", "date_joined": "2020-01-01"},
        )
        serializer.is_valid()

        # Campos read_only não devem ser alterados
        self.assertEqual(serializer.validated_data.get("id"), None)
        self.assertEqual(serializer.validated_data.get("username"), "newuser")


class UserProfileSerializerTestCase(TestCase):
    """Testes para UserProfileSerializer."""

    def setUp(self):
        """Configuração inicial."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_profile_serializer_update(self):
        """Testa atualização de perfil do usuário."""
        serializer = UserProfileSerializer(
            self.user,
            data={
                "email": "newemail@example.com",
                "first_name": "New",
                "last_name": "Name",
            },
            partial=True,
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")

    def test_user_profile_serializer_read_only_fields(self):
        """Testa se campos somente leitura não podem ser editados."""
        original_username = self.user.username
        serializer = UserProfileSerializer(
            self.user, data={"username": "newusername", "is_active": False}
        )
        serializer.is_valid()
        serializer.save()

        self.user.refresh_from_db()
        # username e is_active são read_only, não devem mudar
        self.assertEqual(self.user.username, original_username)
        self.assertTrue(self.user.is_active)
