"""Testes de autenticação JWT do app accounts (login, refresh, verify)."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class JWTAuthenticationTestCase(TestCase):
    """Testes para autenticação JWT."""

    def setUp(self):
        """Configuração inicial."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_token_obtain_pair_success(self):
        """Testa obtenção de token JWT com credenciais válidas."""
        response = self.client.post(
            "/api/token/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_pair_invalid_credentials(self):
        """Testa obtenção de token com credenciais inválidas."""
        response = self.client.post(
            "/api/token/",
            {"username": "testuser", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_obtain_pair_missing_fields(self):
        """Testa obtenção de token com campos faltando."""
        response = self.client.post(
            "/api/token/", {"username": "testuser"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh_success(self):
        """Testa refresh de token com refresh token válido."""
        # Primeiro obtém o token
        token_response = self.client.post(
            "/api/token/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        refresh_token = token_response.data["refresh"]

        # Depois faz refresh
        response = self.client.post(
            "/api/token/refresh/", {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_invalid_token(self):
        """Testa refresh de token com refresh token inválido."""
        response = self.client.post(
            "/api/token/refresh/", {"refresh": "invalid_token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_verify_success(self):
        """Testa verificação de token com token válido."""
        # Primeiro obtém o token
        token_response = self.client.post(
            "/api/token/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        access_token = token_response.data["access"]

        # Depois verifica
        response = self.client.post(
            "/api/token/verify/", {"token": access_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_verify_invalid_token(self):
        """Testa verificação de token com token inválido."""
        response = self.client.post(
            "/api/token/verify/", {"token": "invalid_token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_request_with_token(self):
        """Testa requisição autenticada usando token JWT."""
        # Obtém token
        token_response = self.client.post(
            "/api/token/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        access_token = token_response.data["access"]

        # Faz requisição autenticada
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get("/api/users/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
