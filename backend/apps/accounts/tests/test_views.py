"""
Testes para views do app accounts.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserProfileViewTestCase(TestCase):
    """Testes para UserProfileView."""

    def setUp(self):
        """Configuração inicial."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_get_profile_requires_authentication(self):
        """Testa se GET /api/users/profile/ requer autenticação."""
        response = self.client.get("/api/users/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_authenticated(self):
        """Testa GET /api/users/profile/ com autenticação."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/users/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_update_profile_authenticated(self):
        """Testa atualização de perfil com autenticação."""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            "/api/users/profile/",
            {"email": "updated@example.com", "first_name": "Updated"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.first_name, "Updated")


class UserDetailViewTestCase(TestCase):
    """Testes para UserDetailView."""

    def setUp(self):
        """Configuração inicial."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )

    def test_get_user_detail_requires_authentication(self):
        """Testa se GET /api/users/<id>/ requer autenticação."""
        response = self.client.get(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_authenticated(self):
        """Testa GET /api/users/<id>/ com autenticação."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "otheruser")
