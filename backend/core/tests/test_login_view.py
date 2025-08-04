import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# ============================================================================
# TESTES ORIGINAIS (LoginView antiga)
# ============================================================================

@pytest.mark.django_db
@patch("core.views.sankhya_login")
def test_login_success(mock_sankhya_login):
    """
    Testa login bem-sucedido na LoginView customizada (integração com Sankhya).
    """
    # Cria o usuário previamente (como faria o admin)
    User.objects.create_user(
        email="user@example.com", 
        password="senha123", 
        role="auditor"
    )
    
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

# ============================================================================
# TESTES NOVOS (LoginView atualizada)
# ============================================================================

@pytest.mark.django_db
def test_login_user_not_registered():
    """
    Testa login de usuário não cadastrado no sistema.
    """
    client = APIClient()
    url = reverse("login")
    data = {"email": "unregistered@example.com", "password": "senha123"}
    response = client.post(url, data)
    assert response.status_code == 401
    assert "não cadastrado" in str(response.data["detail"])

@pytest.mark.django_db
def test_login_user_inactive():
    """
    Testa login de usuário desativado.
    """
    User.objects.create_user(
        email="inactive@example.com", 
        password="senha123", 
        role="auditor",
        is_active=False
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "inactive@example.com", "password": "senha123"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        response = client.post(url, data)
    
    assert response.status_code == 401
    assert "desativado" in str(response.data["detail"])

@pytest.mark.django_db
def test_login_admin_local_success():
    """
    Testa login local bem-sucedido para administrador.
    """
    User.objects.create_user(
        email="admin@example.com", 
        password="senha123", 
        role="admin"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "admin@example.com", "password": "senha123"}
    response = client.post(url, data)
    
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["email"] == "admin@example.com"
    assert response.data["role"] == "admin"
    assert response.data["login_type"] == "local"

@pytest.mark.django_db
def test_login_admin_local_failure_sankhya_success():
    """
    Testa login de admin com falha local mas sucesso no Sankhya.
    """
    User.objects.create_user(
        email="admin@example.com", 
        password="senha123", 
        role="admin"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "admin@example.com", "password": "senhaerrada"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        response = client.post(url, data)
    
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["email"] == "admin@example.com"
    assert response.data["role"] == "admin"
    assert response.data["login_type"] == "sankhya"
    
    # Verifica se a senha foi atualizada
    admin = User.objects.get(email="admin@example.com")
    assert admin.check_password("senhaerrada")

@pytest.mark.django_db
def test_login_admin_both_failures():
    """
    Testa login de admin com falha tanto local quanto no Sankhya.
    """
    User.objects.create_user(
        email="admin@example.com", 
        password="senha123", 
        role="admin"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "admin@example.com", "password": "senhaerrada"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = None
        response = client.post(url, data)
    
    assert response.status_code == 401
    assert "Senha incorreta" in str(response.data["detail"])

@pytest.mark.django_db
@patch("core.views.sankhya_login")
def test_login_operational_user_sankhya_success(mock_sankhya_login):
    """
    Testa login bem-sucedido de usuário operacional no Sankhya.
    """
    mock_sankhya_login.return_value = "token_sankhya"
    User.objects.create_user(
        email="auditor@example.com", 
        password="senha123", 
        role="auditor"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "auditor@example.com", "password": "senha123"}
    response = client.post(url, data)
    
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["email"] == "auditor@example.com"
    assert response.data["role"] == "auditor"
    assert response.data["login_type"] == "sankhya"
    
    # Verifica se a senha foi atualizada
    user = User.objects.get(email="auditor@example.com")
    assert user.check_password("senha123")

@pytest.mark.django_db
@patch("core.views.sankhya_login")
def test_login_operational_user_sankhya_failure(mock_sankhya_login):
    """
    Testa login de usuário operacional com falha no Sankhya.
    """
    mock_sankhya_login.return_value = None
    User.objects.create_user(
        email="auditor@example.com", 
        password="senha123", 
        role="auditor"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "auditor@example.com", "password": "senhaerrada"}
    response = client.post(url, data)
    
    assert response.status_code == 401
    assert "inválidos no Sankhya" in str(response.data["detail"])

@pytest.mark.django_db
def test_login_email_normalization():
    """
    Testa se o email é normalizado (convertido para lowercase).
    """
    # Cria o usuário com email normalizado (como o Django faria)
    User.objects.create_user(
        email="user@example.com", 
        password="senha123", 
        role="auditor"
    )
    
    client = APIClient()
    url = reverse("login")
    # Envia email em maiúsculo, mas a LoginView deve normalizar para lowercase
    data = {"email": "USER@EXAMPLE.COM", "password": "senha123"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        response = client.post(url, data)
    
    assert response.status_code == 200
    # Verifica se o email retornado está em lowercase (normalizado)
    assert response.data["email"] == "user@example.com"

@pytest.mark.django_db
def test_login_manager_role():
    """
    Testa login de usuário com role manager (deve usar Sankhya).
    """
    User.objects.create_user(
        email="manager@example.com", 
        password="senha123", 
        role="manager"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "manager@example.com", "password": "senha123"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        response = client.post(url, data)
    
    assert response.status_code == 200
    assert response.data["role"] == "manager"
    assert response.data["login_type"] == "sankhya"

@pytest.mark.django_db
def test_login_password_update_on_sankhya():
    """
    Testa se a senha é atualizada quando o login no Sankhya é bem-sucedido.
    """
    User.objects.create_user(
        email="user@example.com", 
        password="senhaantiga", 
        role="auditor"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "user@example.com", "password": "novasenha"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        response = client.post(url, data)
    
    assert response.status_code == 200
    
    # Verifica se a senha foi atualizada
    user = User.objects.get(email="user@example.com")
    assert user.check_password("novasenha")
    assert user.sankhya_password == "novasenha"

@pytest.mark.django_db
def test_login_cache_token():
    """
    Testa se o token Sankhya é armazenado no cache.
    """
    user = User.objects.create_user(
        email="user@example.com", 
        password="senha123", 
        role="auditor"
    )
    
    client = APIClient()
    url = reverse("login")
    data = {"email": "user@example.com", "password": "senha123"}
    
    with patch("core.views.sankhya_login") as mock_sankhya_login:
        mock_sankhya_login.return_value = "token_sankhya"
        with patch("core.views.cache.set") as mock_cache_set:
            response = client.post(url, data)
    
    assert response.status_code == 200
    mock_cache_set.assert_called_once_with(
        f'sankhya_token_{user.id}', 
        "token_sankhya", 
        timeout=60*60
    )