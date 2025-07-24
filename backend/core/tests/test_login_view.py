import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
@patch("core.views.sankhya_login")
def test_login_success(mock_sankhya_login):
    """
    Testa login bem-sucedido na LoginView customizada (integração com Sankhya).
    """
    mock_sankhya_login.return_value = "token_sankhya"
    client = APIClient()
    url = reverse("login")
    data = {"email": "user@example.com", "password": "senha123"}
    response = client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["email"] == "user@example.com"
    user = User.objects.get(email="user@example.com")
    assert user.sankhya_password == "senha123"

@pytest.mark.django_db
@patch("core.views.sankhya_login")
def test_login_invalid_sankhya(mock_sankhya_login):
    """
    Testa login com falha de autenticação no Sankhya (retorna 401).
    """
    mock_sankhya_login.return_value = None
    client = APIClient()
    url = reverse("login")
    data = {"email": "user@example.com", "password": "senhaerrada"}
    response = client.post(url, data)
    assert response.status_code == 401
    assert "detail" in response.data

@pytest.mark.django_db
def test_login_missing_fields():
    """
    Testa login com campos obrigatórios ausentes (retorna 400).
    """
    client = APIClient()
    url = reverse("login")
    response = client.post(url, {"email": ""})
    assert response.status_code == 400
    assert "detail" in response.data

@pytest.mark.django_db
def test_token_refresh_user_deleted():
    """
    Testa se o refresh token retorna 401 quando o usuário não existe mais no banco.
    """
    user = User.objects.create_user(email="refreshuser@example.com", password="senha123")
    client = APIClient()
    login_url = reverse("login")
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        login_resp = client.post(login_url, {"email": "refreshuser@example.com", "password": "senha123"})
    refresh_token = login_resp.data["refresh"]
    user.delete()
    refresh_url = reverse("token_refresh")
    resp = client.post(refresh_url, {"refresh": refresh_token})
    assert resp.status_code == 401
    assert "detail" in resp.data
    assert "not found" in resp.data["detail"].lower() or "invalid" in resp.data["detail"].lower()