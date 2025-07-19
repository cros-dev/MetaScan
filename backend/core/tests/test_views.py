import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Cavalete, Slot

User = get_user_model()

@pytest.mark.django_db
def test_create_cavalete_authenticated_user():
    user = User.objects.create_user(email="user2@example.com", password="senha123", is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("cavalete-list")
    data = {"status": "available"}
    response = client.post(url, data, format="json")
    print("Cavalete create response:", response.data)
    assert response.status_code == 201, response.data
    assert "id" in response.data
    assert "code" in response.data
    assert response.data["name"].startswith("Cavalete ")

@pytest.mark.django_db
@patch("core.services.sankhya_product.consult_sankhya_product")
def test_update_slot_product_success(mock_consult):
    mock_consult.return_value = {"code": "202118", "description": "ALICATE MULTIUSO"}
    user = User.objects.create_user(email="user3@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste", code="CAV99")
    # noinspection PyUnresolvedReferences
    slot = Slot.objects.create(cavalete=cavalete, side="A", number=1)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("slot-detail", args=[slot.id])
    data = {"product_code": "202118", "quantity": 5, "action": "edited"}
    response = client.patch(url, data)
    print("Slot update success response:", response.data)
    assert response.status_code == 200
    slot.refresh_from_db()
    assert slot.product_code == "202118"
    assert slot.product_description == "ALICATE MULTIUSO"
    assert slot.quantity == 5

@pytest.mark.django_db
@patch("core.services.sankhya_product.consult_sankhya_product")
def test_update_slot_product_invalid_code(mock_consult):
    mock_consult.return_value = None
    user = User.objects.create_user(email="user4@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste2", code="CAV98")
    # noinspection PyUnresolvedReferences
    slot = Slot.objects.create(cavalete=cavalete, side="B", number=2)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("slot-detail", args=[slot.id])
    data = {"product_code": "999999", "quantity": 1, "action": "edited"}
    response = client.patch(url, data)
    print("Slot update invalid code response:", response.data)
    assert response.status_code == 400
    err = response.data["product_code"]
    if isinstance(err, list):
        assert "detail" in err[0]
    else:
        assert "detail" in err 