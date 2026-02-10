"""Testes do módulo product do client Sankhya."""

from unittest.mock import patch

import pytest
from django.conf import settings

from clients.sankhya.exceptions import SankhyaProductError
from clients.sankhya.product import get_product


class TestGetProduct:
    """GET /v1/produtos/{codigoProduto}."""

    def test_raises_when_base_url_empty(self):
        """Raises SankhyaProductError quando SANKHYA_API_BASE_URL não configurado."""
        with patch.object(settings, "SANKHYA_API_BASE_URL", ""):
            with pytest.raises(SankhyaProductError):
                get_product(123, "bearer")

    @patch("clients.sankhya.product.requests.get")
    def test_returns_dict_on_200(self, mock_get):
        """Retorna dict da API quando status 200."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "codigoProduto": 123,
            "nome": "Produto X",
        }
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            result = get_product(123, "bearer")
        assert result == {"codigoProduto": 123, "nome": "Produto X"}
        mock_get.assert_called_once()
        call_kw = mock_get.call_args[1]
        assert call_kw["headers"]["Authorization"] == "Bearer bearer"

    @patch("clients.sankhya.product.requests.get")
    def test_raises_on_404(self, mock_get):
        """Raises SankhyaProductError quando status 404."""
        mock_get.return_value.status_code = 404
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with pytest.raises(SankhyaProductError):
                get_product(999, "bearer")

    @patch("clients.sankhya.product.requests.get")
    def test_raises_on_500(self, mock_get):
        """Raises SankhyaProductError quando status 500."""
        mock_get.return_value.status_code = 500
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with pytest.raises(SankhyaProductError):
                get_product(123, "bearer")

    @patch("clients.sankhya.product.requests.get")
    def test_raises_on_request_exception(self, mock_get):
        """Raises SankhyaProductError em caso de RequestException."""
        import requests

        mock_get.side_effect = requests.RequestException("timeout")
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with pytest.raises(SankhyaProductError):
                get_product(123, "bearer")

    @patch("clients.sankhya.product.requests.get")
    def test_raises_on_non_json_response(self, mock_get):
        """Raises SankhyaProductError quando resposta não é JSON."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value.text = "<html>error</html>"
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with pytest.raises(SankhyaProductError):
                get_product(123, "bearer")
