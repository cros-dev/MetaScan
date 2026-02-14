import pytest
from apps.accounts.models import User
from apps.cavaletes.models import Cavalete, Slot


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def manager_user():
    return User.objects.create_user(
        username="manager",
        email="manager@test.com",
        password="password",
        role=User.Role.MANAGER,
    )


@pytest.fixture
def auditor_user():
    return User.objects.create_user(
        username="auditor",
        email="auditor@test.com",
        password="password",
        role=User.Role.AUDITOR,
    )


@pytest.fixture
def cavalete(manager_user):
    return Cavalete.objects.create(
        code="CAV-001",
        type=Cavalete.Type.DEFAULT,
        user=manager_user,
        status=Cavalete.Status.AVAILABLE,
    )


@pytest.fixture
def another_cavalete(manager_user):
    return Cavalete.objects.create(
        code="CAV-002",
        type=Cavalete.Type.DEFAULT,
        user=manager_user,
        status=Cavalete.Status.AVAILABLE,
    )


@pytest.fixture
def slot(cavalete):
    return Slot.objects.create(
        cavalete=cavalete, side=Slot.Side.SIDE_A, number=1, status=Slot.Status.AVAILABLE
    )
