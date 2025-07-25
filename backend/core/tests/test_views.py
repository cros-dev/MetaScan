import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Cavalete, Slot

User = get_user_model()

@pytest.mark.django_db
def test_create_cavalete_authenticated_user():
    """
    Garante que um usuário autenticado e staff consegue criar um cavalete
    e que os campos obrigatórios são retornados corretamente na resposta.
    """
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
    assert "occupancy" in response.data
    # O valor inicial deve ser 0/12 0%
    assert response.data["occupancy"] == "0/12 0%"

@pytest.mark.django_db
@patch("core.services.sankhya_product.consult_sankhya_product")
def test_update_slot_product_success(mock_consult):
    """
    Garante que é possível atualizar o produto de um slot com código válido,
    e que a descrição do produto é preenchida corretamente.
    """
    mock_consult.return_value = {"code": "202118", "description": "ALICATE MULTIUSO"}
    user = User.objects.create_user(email="user3@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste", code="CAV99")
    # noinspection PyUnresolvedReferences
    slot = Slot.objects.create(cavalete=cavalete, side="A", number=1, status="auditing")
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
    """
    Garante que ao tentar atualizar o produto de um slot com código inválido,
    a API retorna erro 400 e mensagem de produto não encontrado.
    """
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

@pytest.mark.django_db
def test_update_slot_status_blocked():
    """
    Garante que não é possível alterar o campo 'status' do slot via update padrão (PATCH),
    apenas via actions customizadas. Deve retornar erro 400.
    """
    user = User.objects.create_user(email="user5@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste3", code="CAV97")
    # noinspection PyUnresolvedReferences
    slot = Slot.objects.create(cavalete=cavalete, side="A", number=3, status="available")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("slot-detail", args=[slot.id])
    data = {"status": "completed"}
    response = client.patch(url, data)
    print("Slot update status blocked response:", response.data)
    assert response.status_code == 400
    assert "status" in str(response.data).lower() or "só pode ser alterado" in str(response.data).lower()

@pytest.mark.django_db
def test_update_cavalete_status_blocked():
    """
    Garante que não é possível alterar o campo 'status' do cavalete via update padrão (PATCH),
    apenas via actions customizadas. Deve retornar erro 400.
    """
    user = User.objects.create_user(email="user6@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste4", code="CAV96", status="available")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("cavalete-detail", args=[cavalete.id])
    data = {"status": "assigned"}
    response = client.patch(url, data)
    print("Cavalete update status blocked response:", response.data)
    assert response.status_code == 400
    assert "status" in str(response.data).lower() or "só pode ser alterado" in str(response.data).lower()

@pytest.mark.django_db
@patch("core.services.sankhya_product.consult_sankhya_product")
def test_update_slot_product_blocked_if_not_auditing(mock_consult):
    """
    Garante que NÃO é possível atualizar os campos de produto do slot
    quando o status não for 'auditing'.
    Deve retornar erro 400 e mensagem clara.
    """
    mock_consult.return_value = {"code": "202119", "description": "QUALQUER PRODUTO"}
    user = User.objects.create_user(email="user7@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste5", code="CAV95")
    for i, status in enumerate(['available', 'awaiting_approval', 'completed']):
        # noinspection PyUnresolvedReferences
        slot = Slot.objects.create(cavalete=cavalete, side="A", number=4 + i, status=status)
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("slot-detail", args=[slot.id])
        data = {"product_code": "202119", "quantity": 10}
        response = client.patch(url, data)
        print(f"Slot update product blocked (status={status}) response:", response.data)
        assert response.status_code == 400
        assert "só é permitido atualizar produto" in str(response.data).lower()

@pytest.mark.django_db
@patch("core.services.sankhya_product.consult_sankhya_product")
def test_update_slot_product_allowed_auditing(mock_consult):
    """
    Garante que é possível atualizar os campos de produto do slot
    quando o status é 'auditing'.
    Deve retornar sucesso e atualizar os dados corretamente.
    """
    mock_consult.return_value = {"code": "202120", "description": "CHAVE DE FENDA"}
    user = User.objects.create_user(email="user8@example.com", password="senha123", is_staff=True)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste6", code="CAV94")
    # noinspection PyUnresolvedReferences
    slot = Slot.objects.create(cavalete=cavalete, side="B", number=5, status="auditing")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("slot-detail", args=[slot.id])
    data = {"product_code": "202120", "quantity": 3, "action": "edited"}
    response = client.patch(url, data)
    print("Slot update product allowed (auditing) response:", response.data)
    assert response.status_code == 200
    slot.refresh_from_db()
    assert slot.product_code == "202120"
    assert slot.product_description == "CHAVE DE FENDA"
    assert slot.quantity == 3 

@pytest.mark.django_db
def test_cavalete_filter_by_code():
    """
    Garante que é possível filtrar Cavalete por code e que filtro por name não funciona mais.
    """
    user = User.objects.create_user(email="user9@example.com", password="senha123", is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)
    # noinspection PyUnresolvedReferences
    Cavalete.objects.create(name="Cavalete Alpha", code="CAV01")
    # noinspection PyUnresolvedReferences
    Cavalete.objects.create(name="Cavalete Beta", code="CAV02")
    url = reverse("cavalete-list")
    response = client.get(url + "?code=CAV01")
    assert response.status_code == 200
    results = response.data["results"] if "results" in response.data else response.data
    assert any(c["code"] == "CAV01" for c in results)
    response = client.get(url + "?search=02")
    assert response.status_code == 200
    results = response.data["results"] if "results" in response.data else response.data
    assert any(c["code"] == "CAV02" for c in results)
    response = client.get(url + "?name=Cavalete Alpha")
    assert response.status_code == 200
    results = response.data["results"] if "results" in response.data else response.data
    assert not any(c["name"] == "Cavalete Alpha" for c in results)