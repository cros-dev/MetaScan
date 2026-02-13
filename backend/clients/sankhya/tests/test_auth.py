"""Testes do módulo auth do client Sankhya."""

from unittest.mock import patch

import pytest
from django.conf import settings

from clients.sankhya.auth import get_valid_token, login, refresh_token_if_needed
from clients.sankhya.exceptions import SankhyaAuthError


@pytest.mark.django_db
class TestLogin:
    """Login legado (POST /login)."""

    @patch("clients.sankhya.auth.settings")
    def test_login_raises_when_settings_missing(self, mock_settings):
        """Raises SankhyaAuthError quando credenciais ausentes no settings."""
        # Simula ausência de variáveis
        mock_settings.SANKHYA_API_BASE_URL = ""
        mock_settings.SANKHYA_APPKEY = ""
        mock_settings.SANKHYA_TOKEN = ""
        mock_settings.SANKHYA_USER = ""
        mock_settings.SANKHYA_PASSWORD = ""
        
        with pytest.raises(SankhyaAuthError) as exc:
            login()
        assert "Credenciais Sankhya incompletas" in str(exc.value)

    @patch("clients.sankhya.auth.requests.post")
    def test_login_returns_bearer_on_200(self, mock_post):
        """Retorna bearerToken quando resposta 200 com bearerToken."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"bearerToken": "abc123_service", "error": None}
        
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    with patch.object(settings, "SANKHYA_USER", "service_user"):
                        with patch.object(settings, "SANKHYA_PASSWORD", "service_pass"):
                            assert login() == "abc123_service"

    @patch("clients.sankhya.auth.requests.post")
    def test_login_raises_on_non_200(self, mock_post):
        """Raises SankhyaAuthError quando status != 200."""
        mock_post.return_value.status_code = 401
        
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    with patch.object(settings, "SANKHYA_USER", "user"):
                        with patch.object(settings, "SANKHYA_PASSWORD", "pass"):
                            with pytest.raises(SankhyaAuthError):
                                login()


@pytest.mark.django_db
class TestGetValidToken:
    """get_valid_token (cache + renovação)."""

    @patch("clients.sankhya.auth.cache")
    @patch("clients.sankhya.auth.login")
    def test_returns_cached_token_when_exists(self, mock_login, mock_cache):
        """Retorna token do cache quando existir."""
        mock_cache.get.return_value = "cached_bearer_service"
        
        assert get_valid_token() == "cached_bearer_service"
        mock_login.assert_not_called()

    @patch("clients.sankhya.auth.cache")
    @patch("clients.sankhya.auth.login")
    def test_calls_login_and_caches_when_no_cache(self, mock_login, mock_cache):
        """Chama login e grava no cache quando cache vazio."""
        mock_cache.get.return_value = None
        mock_login.return_value = "new_bearer_service"
        
        assert get_valid_token() == "new_bearer_service"
        mock_login.assert_called_once()
        mock_cache.set.assert_called_once()

    @patch("clients.sankhya.auth.cache")
    @patch("clients.sankhya.auth.login")
    def test_raises_when_login_raises(self, mock_login, mock_cache):
        """Raises SankhyaAuthError quando login levanta exceção."""
        mock_cache.get.return_value = None
        mock_login.side_effect = SankhyaAuthError("Login falhou.")
        
        with pytest.raises(SankhyaAuthError):
            get_valid_token()


@pytest.mark.django_db
class TestRefreshTokenIfNeeded:
    """refresh_token_if_needed (limpa cache em 401/403)."""

    @patch("clients.sankhya.auth.cache")
    def test_deletes_cache_and_returns_true_on_401(self, mock_cache):
        """Limpa cache e retorna True para status 401."""
        assert refresh_token_if_needed(401) is True
        mock_cache.delete.assert_called_once_with("sankhya:v1:token:service_user")

    @patch("clients.sankhya.auth.cache")
    def test_deletes_cache_and_returns_true_on_403(self, mock_cache):
        """Limpa cache e retorna True para status 403."""
        assert refresh_token_if_needed(403) is True
        mock_cache.delete.assert_called_once()

    @patch("clients.sankhya.auth.cache")
    def test_returns_false_on_200(self, mock_cache):
        """Retorna False e não mexe no cache para status 200."""
        assert refresh_token_if_needed(200) is False
        mock_cache.delete.assert_not_called()
