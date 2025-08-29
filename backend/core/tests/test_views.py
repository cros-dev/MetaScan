import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_list_permissions():
    """
    Testa as permissões de acesso à lista de usuários.
    """
    admin = User.objects.create_user(email="admin@exemplo.com", password="senha123", role="admin")
    manager = User.objects.create_user(email="manager@exemplo.com", password="senha123", role="manager")
    auditor = User.objects.create_user(email="auditor@exemplo.com", password="senha123", role="auditor")
    
    client = APIClient()
    
    # Admin pode acessar lista de usuários
    client.force_authenticate(user=admin)
    response = client.get(reverse("user-list"))
    assert response.status_code == 200
    
    # Manager NÃO pode acessar lista de usuários
    client.force_authenticate(user=manager)
    response = client.get(reverse("user-list"))
    assert response.status_code == 403
    
    # Auditor NÃO pode acessar lista de usuários
    client.force_authenticate(user=auditor)
    response = client.get(reverse("user-list"))
    assert response.status_code == 403

@pytest.mark.django_db
def test_me_view_authenticated():
    """
    Testa que o endpoint /me/ retorna dados do usuário autenticado.
    """
    user = User.objects.create_user(email="user@exemplo.com", password="senha123", role="manager")
    client = APIClient()
    client.force_authenticate(user=user)
    
    response = client.get(reverse("me"))
    assert response.status_code == 200
    assert response.data["email"] == user.email
    assert response.data["role"] == user.role

@pytest.mark.django_db
def test_me_view_unauthenticated():
    """
    Testa que o endpoint /me/ requer autenticação.
    """
    client = APIClient()
    response = client.get(reverse("me"))
    assert response.status_code == 401