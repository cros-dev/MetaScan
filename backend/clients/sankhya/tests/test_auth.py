"""Testes do módulo auth do client Sankhya."""

from unittest.mock import MagicMock, patch

import pytest
from django.conf import settings

from clients.sankhya.auth import get_valid_token, login, refresh_token_if_needed
from clients.sankhya.exceptions import SankhyaAuthError


@pytest.mark.django_db
class TestLogin:
    """Login legado (POST /login)."""

    @patch("clients.sankhya.auth.settings")
    def test_login_raises_when_settings_missing(self, mock_settings):
        """Raises SankhyaAuthError quando SANKHYA_API_BASE_URL, APPKEY ou TOKEN ausentes."""
        mock_settings.SANKHYA_API_BASE_URL = ""
        mock_settings.SANKHYA_APPKEY = "key"
        mock_settings.SANKHYA_TOKEN = "tok"
        with pytest.raises(SankhyaAuthError):
            login("u", "p")

    @patch("clients.sankhya.auth.requests.post")
    def test_login_returns_bearer_on_200(self, mock_post):
        """Retorna bearerToken quando resposta 200 com bearerToken."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"bearerToken": "abc123", "error": None}
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    assert login("user", "pass") == "abc123"

    @patch("clients.sankhya.auth.requests.post")
    def test_login_raises_on_non_200(self, mock_post):
        """Raises SankhyaAuthError quando status != 200."""
        mock_post.return_value.status_code = 401
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    with pytest.raises(SankhyaAuthError):
                        login("user", "pass")

    @patch("clients.sankhya.auth.requests.post")
    def test_login_raises_on_request_exception(self, mock_post):
        """Raises SankhyaAuthError em caso de RequestException."""
        import requests

        mock_post.side_effect = requests.RequestException("timeout")
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    with pytest.raises(SankhyaAuthError):
                        login("user", "pass")

    @patch("clients.sankhya.auth.requests.post")
    def test_login_raises_on_non_json_response(self, mock_post):
        """Raises SankhyaAuthError quando resposta não é JSON."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value.text = "<html>error</html>"
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    with pytest.raises(SankhyaAuthError):
                        login("user", "pass")

    @patch("clients.sankhya.auth.requests.post")
    def test_login_raises_when_bearer_absent(self, mock_post):
        """Raises SankhyaAuthError quando resposta 200 mas sem bearerToken."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"bearerToken": None, "error": "unauthorized"}
        with patch.object(settings, "SANKHYA_API_BASE_URL", "https://api.sankhya.com.br"):
            with patch.object(settings, "SANKHYA_APPKEY", "key"):
                with patch.object(settings, "SANKHYA_TOKEN", "tok"):
                    with pytest.raises(SankhyaAuthError):
                        login("user", "pass")


@pytest.mark.django_db
class TestGetValidToken:
    """get_valid_token (cache + renovação)."""

    def test_raises_when_user_has_no_sankhya_password(self):
        """Raises SankhyaAuthError quando user sem sankhya_password."""
        user = MagicMock()
        user.id = 1
        user.email = "u@u.com"
        del user.sankhya_password
        with pytest.raises(SankhyaAuthError):
            get_valid_token(user)

    @patch("clients.sankhya.auth.cache")
    @patch("clients.sankhya.auth.login")
    def test_returns_cached_token_when_exists(self, mock_login, mock_cache):
        """Retorna token do cache quando existir."""
        user = MagicMock(id=1, email="u@u.com", sankhya_password="pass")
        mock_cache.get.return_value = "cached_bearer"
        assert get_valid_token(user) == "cached_bearer"
        mock_login.assert_not_called()

    @patch("clients.sankhya.auth.cache")
    @patch("clients.sankhya.auth.login")
    def test_calls_login_and_caches_when_no_cache(self, mock_login, mock_cache):
        """Chama login e grava no cache quando cache vazio."""
        user = MagicMock(id=1, email="u@u.com", sankhya_password="pass")
        mock_cache.get.return_value = None
        mock_login.return_value = "new_bearer"
        assert get_valid_token(user) == "new_bearer"
        mock_login.assert_called_once_with("u@u.com", "pass")
        mock_cache.set.assert_called_once()

    @patch("clients.sankhya.auth.cache")
    @patch("clients.sankhya.auth.login")
    def test_raises_when_login_raises(self, mock_login, mock_cache):
        """Raises SankhyaAuthError quando login levanta SankhyaAuthError."""
        user = MagicMock(id=1, email="u@u.com", sankhya_password="pass")
        mock_cache.get.return_value = None
        mock_login.side_effect = SankhyaAuthError("Login falhou.")
        with pytest.raises(SankhyaAuthError):
            get_valid_token(user)


@pytest.mark.django_db
class TestRefreshTokenIfNeeded:
    """refresh_token_if_needed (limpa cache em 401/403)."""

    @patch("clients.sankhya.auth.cache")
    def test_deletes_cache_and_returns_true_on_401(self, mock_cache):
        """Limpa cache e retorna True para status 401."""
        user = MagicMock(id=1)
        assert refresh_token_if_needed(user, 401) is True
        mock_cache.delete.assert_called_once_with("sankhya:v1:token:1")

    @patch("clients.sankhya.auth.cache")
    def test_deletes_cache_and_returns_true_on_403(self, mock_cache):
        """Limpa cache e retorna True para status 403."""
        user = MagicMock(id=1)
        assert refresh_token_if_needed(user, 403) is True
        mock_cache.delete.assert_called_once()

    @patch("clients.sankhya.auth.cache")
    def test_returns_false_on_200(self, mock_cache):
        """Retorna False e não mexe no cache para status 200."""
        user = MagicMock(id=1)
        assert refresh_token_if_needed(user, 200) is False
        mock_cache.delete.assert_not_called()
