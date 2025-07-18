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