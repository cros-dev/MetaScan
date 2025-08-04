import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_list_admin_only():
    """
    Garante que apenas administradores podem listar usuários.
    """
    auditor = User.objects.create_user(email="auditor@test.com", password="senha123", role="auditor")
    admin = User.objects.create_user(email="admin@test.com", password="senha123", role="admin")
    client = APIClient()
    
    # Usuário não-admin
    client.force_authenticate(user=auditor)
    url = reverse("user-list")
    response = client.get(url)
    assert response.status_code == 403

    # Usuário admin
    client.force_authenticate(user=admin)
    response = client.get(url)
    assert response.status_code == 200
    assert "results" in response.data or isinstance(response.data, list)

@pytest.mark.django_db
def test_user_create_admin_only():
    """
    Garante que apenas administradores podem criar usuários.
    """
    manager = User.objects.create_user(email="manager@test.com", password="senha123", role="manager")
    admin = User.objects.create_user(email="admin2@test.com", password="senha123", role="admin")
    client = APIClient()
    url = reverse("user-list")
    data = {"email": "newuser@test.com", "role": "auditor"}
    
    # Usuário não-admin
    client.force_authenticate(user=manager)
    response = client.post(url, data, format="json")
    assert response.status_code == 403

    # Usuário admin
    client.force_authenticate(user=admin)
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["email"] == "newuser@test.com"
    assert response.data["role"] == "auditor"

@pytest.mark.django_db
def test_user_create_with_password():
    """
    Garante que usuário é criado com senha criptografada.
    """
    admin = User.objects.create_user(email="admin3@test.com", password="senha123", role="admin")
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-list")
    data = {"email": "newuser2@test.com", "role": "auditor", "password": "minhasenha123"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    
    # Verifica se a senha foi definida
    user = User.objects.get(email="newuser2@test.com")
    assert user.check_password("minhasenha123")

@pytest.mark.django_db
def test_user_create_default_password():
    """
    Garante que usuário é criado com senha padrão quando não fornecida.
    """
    admin = User.objects.create_user(email="admin4@test.com", password="senha123", role="admin")
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-list")
    data = {"email": "newuser3@test.com", "role": "auditor"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    
    # Verifica se a senha padrão foi definida
    user = User.objects.get(email="newuser3@test.com")
    assert user.check_password("123456")

@pytest.mark.django_db
def test_user_update_admin_only():
    """
    Garante que apenas administradores podem atualizar usuários.
    """
    target_user = User.objects.create_user(email="target@test.com", password="senha123", role="auditor")
    manager = User.objects.create_user(email="manager2@test.com", password="senha123", role="manager")
    admin = User.objects.create_user(email="admin5@test.com", password="senha123", role="admin")
    client = APIClient()
    url = reverse("user-detail", args=[target_user.id])
    data = {"role": "manager"}
    
    # Usuário não-admin
    client.force_authenticate(user=manager)
    response = client.patch(url, data, format="json")
    assert response.status_code == 403

    # Usuário admin
    client.force_authenticate(user=admin)
    response = client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["role"] == "manager"

@pytest.mark.django_db
def test_user_update_password():
    """
    Garante que a senha é atualizada corretamente.
    """
    admin = User.objects.create_user(email="admin6@test.com", password="senha123", role="admin")
    target_user = User.objects.create_user(email="target2@test.com", password="senha123", role="auditor")
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-detail", args=[target_user.id])
    data = {"password": "novasenha123"}
    response = client.patch(url, data, format="json")
    assert response.status_code == 200
    
    # Verifica se a senha foi atualizada
    target_user.refresh_from_db()
    assert target_user.check_password("novasenha123")

@pytest.mark.django_db
def test_user_delete_admin_only():
    """
    Garante que apenas administradores podem deletar usuários.
    """
    target_user = User.objects.create_user(email="target3@test.com", password="senha123", role="auditor")
    manager = User.objects.create_user(email="manager3@test.com", password="senha123", role="manager")
    admin = User.objects.create_user(email="admin7@test.com", password="senha123", role="admin")
    client = APIClient()
    url = reverse("user-detail", args=[target_user.id])
    
    # Usuário não-admin
    client.force_authenticate(user=manager)
    response = client.delete(url)
    assert response.status_code == 403

    # Usuário admin
    client.force_authenticate(user=admin)
    response = client.delete(url)
    assert response.status_code == 204
    
    # Verifica se o usuário foi realmente deletado
    assert not User.objects.filter(email="target3@test.com").exists()

@pytest.mark.django_db
def test_user_delete_protect_first_superuser():
    """
    Garante que o primeiro superuser não pode ser deletado.
    """
    # Cria o primeiro superuser
    first_admin = User.objects.create_superuser(email="first@test.com", password="senha123")
    second_admin = User.objects.create_user(email="second@test.com", password="senha123", role="admin")
    
    client = APIClient()
    client.force_authenticate(user=second_admin)
    url = reverse("user-detail", args=[first_admin.id])
    response = client.delete(url)
    assert response.status_code == 400
    assert "administrador padrão" in str(response.data)
    
    # Verifica se o usuário ainda existe
    assert User.objects.filter(email="first@test.com").exists()

@pytest.mark.django_db
def test_user_deactivate_admin_only():
    """
    Garante que apenas administradores podem desativar usuários.
    """
    target_user = User.objects.create_user(email="target4@test.com", password="senha123", role="auditor")
    manager = User.objects.create_user(email="manager4@test.com", password="senha123", role="manager")
    admin = User.objects.create_user(email="admin8@test.com", password="senha123", role="admin")
    client = APIClient()
    url = reverse("user-deactivate", args=[target_user.id])
    
    # Usuário não-admin
    client.force_authenticate(user=manager)
    response = client.post(url)
    assert response.status_code == 403

    # Usuário admin
    client.force_authenticate(user=admin)
    response = client.post(url)
    assert response.status_code == 200
    assert response.data["is_active"] is False
    
    # Verifica se o usuário foi desativado
    target_user.refresh_from_db()
    assert not target_user.is_active

@pytest.mark.django_db
def test_user_deactivate_protect_first_superuser():
    """
    Garante que o primeiro superuser não pode ser desativado.
    """
    # Cria o primeiro superuser
    first_admin = User.objects.create_superuser(email="first2@test.com", password="senha123")
    second_admin = User.objects.create_user(email="second2@test.com", password="senha123", role="admin")
    
    client = APIClient()
    client.force_authenticate(user=second_admin)
    url = reverse("user-deactivate", args=[first_admin.id])
    response = client.post(url)
    assert response.status_code == 400
    assert "administrador padrão" in str(response.data)
    
    # Verifica se o usuário ainda está ativo
    first_admin.refresh_from_db()
    assert first_admin.is_active

@pytest.mark.django_db
def test_user_deactivate_already_inactive():
    """
    Garante que não é possível desativar um usuário já inativo.
    """
    admin = User.objects.create_user(email="admin9@test.com", password="senha123", role="admin")
    target_user = User.objects.create_user(email="target5@test.com", password="senha123", role="auditor", is_active=False)
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-deactivate", args=[target_user.id])
    response = client.post(url)
    assert response.status_code == 400
    assert "já está desativado" in str(response.data)

@pytest.mark.django_db
def test_user_reactivate_admin_only():
    """
    Garante que apenas administradores podem reativar usuários.
    """
    target_user = User.objects.create_user(email="target6@test.com", password="senha123", role="auditor", is_active=False)
    manager = User.objects.create_user(email="manager5@test.com", password="senha123", role="manager")
    admin = User.objects.create_user(email="admin10@test.com", password="senha123", role="admin")
    client = APIClient()
    url = reverse("user-reactivate", args=[target_user.id])
    
    # Usuário não-admin
    client.force_authenticate(user=manager)
    response = client.post(url)
    assert response.status_code == 403

    # Usuário admin
    client.force_authenticate(user=admin)
    response = client.post(url)
    assert response.status_code == 200
    assert response.data["is_active"] is True
    
    # Verifica se o usuário foi reativado
    target_user.refresh_from_db()
    assert target_user.is_active

@pytest.mark.django_db
def test_user_reactivate_protect_first_superuser():
    """
    Garante que o primeiro superuser não pode ser reativado.
    """
    # Cria o primeiro superuser
    first_admin = User.objects.create_superuser(email="first3@test.com", password="senha123")
    second_admin = User.objects.create_user(email="second3@test.com", password="senha123", role="admin")
    
    client = APIClient()
    client.force_authenticate(user=second_admin)
    url = reverse("user-reactivate", args=[first_admin.id])
    response = client.post(url)
    assert response.status_code == 400
    assert "Administrador padrão" in str(response.data)

@pytest.mark.django_db
def test_user_reactivate_already_active():
    """
    Garante que não é possível reativar um usuário já ativo.
    """
    admin = User.objects.create_user(email="admin11@test.com", password="senha123", role="admin")
    target_user = User.objects.create_user(email="target7@test.com", password="senha123", role="auditor", is_active=True)
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-reactivate", args=[target_user.id])
    response = client.post(url)
    assert response.status_code == 400
    assert "já está ativo" in str(response.data)

@pytest.mark.django_db
def test_user_filter_by_role():
    """
    Garante que é possível filtrar usuários por role.
    """
    admin = User.objects.create_user(email="admin12@test.com", password="senha123", role="admin")
    User.objects.create_user(email="auditor1@test.com", password="senha123", role="auditor")
    User.objects.create_user(email="auditor2@test.com", password="senha123", role="auditor")
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-list")
    response = client.get(url, {"role": "auditor"})
    assert response.status_code == 200
    
    # Verifica se apenas auditores foram retornados
    users = response.data["results"] if "results" in response.data else response.data
    assert len(users) == 2
    for user in users:
        assert user["role"] == "auditor"

@pytest.mark.django_db
def test_user_filter_by_is_active():
    """
    Garante que é possível filtrar usuários por status ativo.
    """
    admin = User.objects.create_user(email="admin13@test.com", password="senha123", role="admin")
    User.objects.create_user(email="active@test.com", password="senha123", role="auditor", is_active=True)
    User.objects.create_user(email="inactive@test.com", password="senha123", role="auditor", is_active=False)
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-list")
    response = client.get(url, {"is_active": "true"})
    assert response.status_code == 200
    
    # Verifica se apenas usuários ativos foram retornados
    users = response.data["results"] if "results" in response.data else response.data
    for user in users:
        assert user["is_active"] is True

@pytest.mark.django_db
def test_user_search_by_email():
    """
    Garante que é possível buscar usuários por email.
    """
    admin = User.objects.create_user(email="admin_search@example.com", password="senha123", role="admin")
    User.objects.create_user(email="test1@test.com", password="senha123", role="auditor")
    User.objects.create_user(email="test2@test.com", password="senha123", role="auditor")
    User.objects.create_user(email="other@example.com", password="senha123", role="auditor")
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-list")
    response = client.get(url, {"search": "test"})
    assert response.status_code == 200
    
    # Verifica se apenas usuários com "test" no email foram retornados
    users = response.data["results"] if "results" in response.data else response.data
    assert len(users) == 2
    for user in users:
        assert "test" in user["email"]

@pytest.mark.django_db
def test_user_ordering():
    """
    Garante que é possível ordenar usuários.
    """
    admin = User.objects.create_user(email="admin15@test.com", password="senha123", role="admin")
    User.objects.create_user(email="a@test.com", password="senha123", role="auditor")
    User.objects.create_user(email="c@test.com", password="senha123", role="auditor")
    User.objects.create_user(email="b@test.com", password="senha123", role="auditor")
    
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("user-list")
    response = client.get(url, {"ordering": "email"})
    assert response.status_code == 200
    
    # Verifica se os usuários estão ordenados por email
    users = response.data["results"] if "results" in response.data else response.data
    emails = [user["email"] for user in users if user["email"] != "admin15@test.com"]
    assert emails == sorted(emails)

@pytest.mark.django_db
def test_user_serializer_class_selection():
    """
    Garante que o serializer correto é usado para cada ação.
    """
    admin = User.objects.create_user(email="admin16@test.com", password="senha123", role="admin")
    target_user = User.objects.create_user(email="target8@test.com", password="senha123", role="auditor")
    
    client = APIClient()
    client.force_authenticate(user=admin)
    
    # List deve usar UserSummarySerializer
    url = reverse("user-list")
    response = client.get(url)
    assert response.status_code == 200
    users = response.data["results"] if "results" in response.data else response.data
    if users:
        user = users[0]
        assert "id" in user
        assert "email" in user
        assert "role" in user
        assert "is_active" in user
        # UserSummarySerializer não deve ter password
        assert "password" not in user
    
    # Retrieve deve usar UserSummarySerializer
    url = reverse("user-detail", args=[target_user.id])
    response = client.get(url)
    assert response.status_code == 200
    assert "password" not in response.data
    
    # Update deve usar UserFullSerializer
    data = {"role": "manager"}
    response = client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["role"] == "manager" 