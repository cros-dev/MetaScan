import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.inventory.models import CavaleteHistory, Action
from apps.cavaletes.models import Cavalete


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def manager_user(db):
    return User.objects.create_user(
        username="manager", password="password", role=User.Role.MANAGER
    )


@pytest.fixture
def auditor_user(db):
    return User.objects.create_user(
        username="auditor", password="password", role=User.Role.AUDITOR
    )


@pytest.fixture
def cavalete_history(db, manager_user):
    cavalete = Cavalete.objects.create(code="CAV01", user=manager_user)
    return CavaleteHistory.objects.create(
        cavalete=cavalete, user=manager_user, action=Action.CREATE, description="Teste"
    )


@pytest.mark.django_db
class TestInventoryPermissions:
    def test_manager_can_list_history(self, api_client, manager_user, cavalete_history):
        """Gestor deve conseguir ver o histórico."""
        api_client.force_authenticate(user=manager_user)
        url = "/api/inventory/history/cavaletes/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_auditor_cannot_list_history(self, api_client, auditor_user):
        """Auditor NÃO deve conseguir ver o histórico."""
        api_client.force_authenticate(user=auditor_user)
        url = "/api/inventory/history/cavaletes/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_list_history(self, api_client):
        """Usuário anônimo não acessa histórico."""
        url = "/api/inventory/history/cavaletes/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
