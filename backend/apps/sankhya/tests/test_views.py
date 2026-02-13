"""Testes das views do app Sankhya."""

from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User
from clients.sankhya.exceptions import SankhyaAuthError, SankhyaProductError


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", email="test@test.com", password="password"
    )


@pytest.mark.django_db
class TestProductDetailView:
    """Testes para o endpoint GET /api/sankhya/products/{code}/."""

    def test_get_product_unauthenticated(self, api_client):
        """Requer autenticação."""
        url = reverse("sankhya:product-detail", args=["123"])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("apps.sankhya.views.get_valid_token")
    @patch("apps.sankhya.views.get_product")
    def test_get_product_success(
        self, mock_get_product, mock_get_token, api_client, user
    ):
        """Retorna dados do produto com sucesso."""
        api_client.force_authenticate(user=user)
        mock_get_token.return_value = "bearer_token"
        mock_get_product.return_value = {"codigo": 123, "descricao": "Produto Teste"}

        url = reverse("sankhya:product-detail", args=["123"])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["codigo"] == 123
        assert response.data["descricao"] == "Produto Teste"
        mock_get_token.assert_called_once()
        mock_get_product.assert_called_once_with("123", "bearer_token")

    @patch("apps.sankhya.views.get_valid_token")
    def test_get_product_auth_error(self, mock_get_token, api_client, user):
        """Retorna 503 quando falha autenticação no Sankhya."""
        api_client.force_authenticate(user=user)
        mock_get_token.side_effect = SankhyaAuthError("Falha no login")

        url = reverse("sankhya:product-detail", args=["123"])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "Falha no login" in response.data["detail"]

    @patch("apps.sankhya.views.get_valid_token")
    @patch("apps.sankhya.views.get_product")
    def test_get_product_not_found(
        self, mock_get_product, mock_get_token, api_client, user
    ):
        """Retorna 404 quando produto não existe no Sankhya."""
        api_client.force_authenticate(user=user)
        mock_get_token.return_value = "bearer_token"
        mock_get_product.side_effect = SankhyaProductError("Produto não encontrado.")

        url = reverse("sankhya:product-detail", args=["999"])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Produto não encontrado" in response.data["detail"]

    @patch("apps.sankhya.views.get_valid_token")
    @patch("apps.sankhya.views.get_product")
    def test_get_product_sankhya_error(
        self, mock_get_product, mock_get_token, api_client, user
    ):
        """Retorna 502 quando Sankhya retorna erro genérico."""
        api_client.force_authenticate(user=user)
        mock_get_token.return_value = "bearer_token"
        mock_get_product.side_effect = SankhyaProductError("Erro desconhecido.")

        url = reverse("sankhya:product-detail", args=["123"])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_502_BAD_GATEWAY
