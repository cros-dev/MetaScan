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
    user = User.objects.create_user(email="user2@example.com", password="senha123", role="manager")
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
    assert response.data["occupancy"] == "0/12 0%"

@pytest.mark.django_db
@patch("core.services.sankhya_product.consult_sankhya_product")
def test_update_slot_product_success(mock_consult):
    """
    Garante que é possível atualizar o produto de um slot com código válido,
    e que a descrição do produto é preenchida corretamente.
    """
    mock_consult.return_value = {"code": "202118", "description": "ALICATE MULTIUSO"}
    user = User.objects.create_user(email="user3@example.com", password="senha123", role="manager")
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
    assert response.status_code == 200, response.data
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
    user = User.objects.create_user(email="user4@example.com", password="senha123", role="manager")
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
    assert response.status_code == 400, response.data
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
    user = User.objects.create_user(email="user5@example.com", password="senha123", role="manager")
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
    assert response.status_code == 400, response.data
    assert "status" in str(response.data).lower() or "só pode ser alterado" in str(response.data).lower()

@pytest.mark.django_db
def test_update_cavalete_status_blocked():
    """
    Garante que não é possível alterar o campo 'status' do cavalete via update padrão (PATCH),
    apenas via actions customizadas. Deve retornar erro 400.
    """
    user = User.objects.create_user(email="user6@example.com", password="senha123", role="manager")
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Teste4", code="CAV96", status="available")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("cavalete-detail", args=[cavalete.id])
    data = {"status": "assigned"}
    response = client.patch(url, data)
    print("Cavalete update status blocked response:", response.data)
    assert response.status_code == 400, response.data
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
    user = User.objects.create_user(email="user7@example.com", password="senha123", role="manager")
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
        assert response.status_code == 400, response.data
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
    user = User.objects.create_user(email="user8@example.com", password="senha123", role="manager")
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
    assert response.status_code == 200, response.data
    slot.refresh_from_db()
    assert slot.product_code == "202120"
    assert slot.product_description == "CHAVE DE FENDA"
    assert slot.quantity == 3

@pytest.mark.django_db
def test_cavalete_filter_by_code():
    """
    Garante que é possível filtrar Cavalete por code e que filtro por name não funciona mais.
    """
    user = User.objects.create_user(email="user9@example.com", password="senha123", role="manager")
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

@pytest.mark.django_db
def test_permissions_roles():
    """
    Testa as permissões básicas dos papéis: admin, manager, auditor.
    """
    from django.urls import reverse
    from rest_framework.test import APIClient
    admin = User.objects.create_user(email="admin@exemplo.com", password="senha123", role="admin")
    manager = User.objects.create_user(email="manager@exemplo.com", password="senha123", role="manager")
    auditor = User.objects.create_user(email="auditor@exemplo.com", password="senha123", role="auditor")
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Auditor", code="CAV10", user=auditor)
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=1, status="auditing")
    client = APIClient(); client.force_authenticate(user=admin)
    assert client.get(reverse("cavalete-list")).status_code == 200
    assert client.get(reverse("slot-list")).status_code == 200
    assert client.get(reverse("user-list")).status_code == 200
    client.force_authenticate(user=manager)
    assert client.get(reverse("cavalete-list")).status_code == 200
    assert client.get(reverse("slot-list")).status_code == 200
    assert client.get(reverse("user-list")).status_code == 403
    client.force_authenticate(user=auditor)
    response = client.get(reverse("cavalete-list"))
    cavs = response.json()
    if isinstance(cavs, dict) and "results" in cavs:
        cavs = cavs["results"]
    assert all(c["user"]["id"] == auditor.id for c in cavs if c.get("user"))
    response = client.get(reverse("slot-list"))
    slots = response.json()
    if isinstance(slots, dict) and "results" in slots:
        slots = slots["results"]
    assert all(s["cavalete"] == cavalete.id for s in slots)
    assert client.get(reverse("user-list")).status_code == 403

@pytest.mark.django_db
def test_finish_confirmation_permission():
    """
    Testa que apenas auditor e admin podem finalizar conferência (finish_confirmation).
    """
    from django.urls import reverse
    from rest_framework.test import APIClient
    admin = User.objects.create_user(email="admin2@exemplo.com", password="senha123", role="admin")
    manager = User.objects.create_user(email="manager2@exemplo.com", password="senha123", role="manager")
    auditor = User.objects.create_user(email="auditor2@exemplo.com", password="senha123", role="auditor")
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Auditor2", code="CAV11", user=auditor)
    
    client = APIClient()
    
    # Teste 1: Auditor pode finalizar conferência
    # noinspection PyUnresolvedReferences
    slot_auditor = Slot.objects.create(cavalete=cavalete, side="A", number=1, status="auditing")
    url_auditor = reverse("slot-finish-confirmation", args=[slot_auditor.id])
    client.force_authenticate(user=auditor)
    response_auditor = client.post(url_auditor)
    assert response_auditor.status_code in (200, 201), f"Auditor deveria poder finalizar. Status: {response_auditor.status_code}, Data: {response_auditor.data}"
    
    # Teste 2: Manager NÃO pode finalizar conferência (403 Forbidden)
    # noinspection PyUnresolvedReferences
    slot_manager = Slot.objects.create(cavalete=cavalete, side="A", number=2, status="auditing")
    url_manager = reverse("slot-finish-confirmation", args=[slot_manager.id])
    client.force_authenticate(user=manager)
    response_manager = client.post(url_manager)
    assert response_manager.status_code == 403, f"Manager não deveria poder finalizar. Status: {response_manager.status_code}, Data: {response_manager.data}"
    
    # Teste 3: Admin pode finalizar conferência
    # noinspection PyUnresolvedReferences
    slot_admin = Slot.objects.create(cavalete=cavalete, side="A", number=3, status="auditing")
    url_admin = reverse("slot-finish-confirmation", args=[slot_admin.id])
    client.force_authenticate(user=admin)
    response_admin = client.post(url_admin)
    assert response_admin.status_code in (200, 201), f"Admin deveria poder finalizar. Status: {response_admin.status_code}, Data: {response_admin.data}"

@pytest.mark.django_db
def test_occupancy_only_completed():
    """
    Garante que occupancy só considera slots com status 'completed' como ocupados.
    """
    user = User.objects.create_user(email="userocc@exemplo.com", password="senha123", role="manager")
    client = APIClient(); client.force_authenticate(user=user)
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Occ", code="CAV20", user=user)
    for i in range(1, 4):
        # noinspection PyUnresolvedReferences
        Slot.objects.create(cavalete=cavalete, side="A", number=i, status="completed")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=4, status="auditing")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=5, status="auditing")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=6, status="available")
    url = reverse("cavalete-detail", args=[cavalete.id])
    response = client.get(url)
    assert response.status_code == 200
    occ = response.data["occupancy"]
    assert occ == "3/6 50%", f"Esperado 3/6 50%, veio {occ}"

@pytest.mark.django_db
def test_slots_ordered_by_number():
    """
    Garante que os slots são sempre retornados ordenados por número em ordem crescente,
    independente da ordem de criação ou atualização.
    """
    user = User.objects.create_user(email="user_order@example.com", password="senha123", role="manager")
    # noinspection PyUnresolvedReferences
    cavalete = Cavalete.objects.create(name="Cavalete Ordem", code="CAV99")
    
    # Criar slots em ordem aleatória
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=3, status="available")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=1, status="available")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=5, status="available")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=2, status="available")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=4, status="available")
    # noinspection PyUnresolvedReferences
    Slot.objects.create(cavalete=cavalete, side="A", number=6, status="available")
    
    client = APIClient()
    client.force_authenticate(user=user)
    
    # Testar ordenação no endpoint de cavaletes
    url = reverse("cavalete-detail", args=[cavalete.id])
    response = client.get(url)
    assert response.status_code == 200, response.data
    
    slots = response.data['slots']
    assert len(slots) == 6
    
    # Verificar se estão ordenados por número
    slot_numbers = [slot['number'] for slot in slots]
    expected_order = [1, 2, 3, 4, 5, 6]
    assert slot_numbers == expected_order, f"Slots não estão ordenados. Esperado: {expected_order}, Obtido: {slot_numbers}"
    
    # Testar ordenação no endpoint de slots
    url_slots = reverse("slot-list")
    response_slots = client.get(url_slots, {'cavalete': cavalete.id})
    assert response_slots.status_code == 200, response_slots.data
    
    # Verificar se a resposta é paginada
    if 'results' in response_slots.data:
        slots_list = response_slots.data['results']
    else:
        slots_list = response_slots.data
    
    slot_numbers_list = [slot['number'] for slot in slots_list if slot['cavalete'] == cavalete.id]
    assert slot_numbers_list == expected_order, f"Slots no endpoint /slots/ não estão ordenados. Esperado: {expected_order}, Obtido: {slot_numbers_list}"