import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from apps.cavaletes.models import Slot
from apps.cavaletes import messages


@pytest.mark.django_db
class TestCavaleteViewSet:
    """Testes para CavaleteViewSet."""

    def test_list_cavaletes_manager(
        self, api_client, manager_user, cavalete, another_cavalete
    ):
        """Gestor deve ver todos os cavaletes."""
        api_client.force_authenticate(user=manager_user)
        url = reverse("cavaletes:cavalete-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2

    def test_list_cavaletes_auditor_assigned(
        self, api_client, auditor_user, cavalete, another_cavalete
    ):
        """Conferente deve ver apenas cavaletes atribuídos a ele."""
        cavalete.user = auditor_user
        cavalete.save()

        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:cavalete-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == cavalete.id

    def test_create_cavalete_manager(self, api_client, manager_user):
        """Gestor pode criar cavalete."""
        api_client.force_authenticate(user=manager_user)
        url = reverse("cavaletes:cavalete-list")
        data = {"code": "C001", "name": "Cavalete Teste"}

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_cavalete_auditor_forbidden(self, api_client, auditor_user):
        """Conferente NÃO pode criar cavalete."""
        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:cavalete-list")
        data = {"code": "C002", "name": "Cavalete Proibido"}

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestSlotWorkflow:
    """Testes para o workflow de Slots."""

    def test_start_confirmation_creates_history(self, api_client, auditor_user, slot):
        """Deve criar histórico ao iniciar conferência."""
        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:slot-start-confirmation", args=[slot.id])

        api_client.post(url)

        assert slot.history.count() == 1
        history = slot.history.first()
        assert history.action == "START_AUDIT"
        assert history.user == auditor_user

    def test_finish_confirmation_creates_history(self, api_client, auditor_user, slot):
        """Deve criar histórico ao finalizar conferência."""
        slot.status = Slot.Status.AUDITING
        slot.save()

        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:slot-finish-confirmation", args=[slot.id])

        api_client.post(url)

        assert slot.history.count() == 1
        assert slot.history.first().action == "FINISH_AUDIT"

    def test_edit_slot_creates_history(self, api_client, auditor_user, slot):
        """Deve criar histórico ao editar slot."""
        slot.status = Slot.Status.AUDITING
        slot.quantity = 5
        slot.product_code = "OLD"
        slot.save()

        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:slot-detail", args=[slot.id])
        data = {"quantity": 10, "product_code": "NEW"}

        api_client.patch(url, data)

        assert slot.history.count() == 1
        history = slot.history.first()
        assert history.action == "UPDATE"
        assert history.old_quantity == 5
        assert history.new_quantity == 10
        assert history.old_product_code == "OLD"
        assert history.new_product_code == "NEW"

    def test_finish_confirmation(self, api_client, auditor_user, slot):
        """Deve finalizar a conferência (AUDITING -> COMPLETED)."""
        slot.status = Slot.Status.AUDITING
        slot.save()

        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:slot-finish-confirmation", args=[slot.id])

        response = api_client.post(url)

        slot.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert slot.status == Slot.Status.COMPLETED

    def test_edit_slot_product_during_audit(self, api_client, auditor_user, slot):
        """Conferente pode editar produto/quantidade se status for AUDITING."""
        slot.status = Slot.Status.AUDITING
        slot.save()

        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:slot-detail", args=[slot.id])
        data = {"quantity": 10, "product_code": "P123"}

        response = api_client.patch(url, data)

        slot.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert slot.quantity == 10
        assert slot.product_code == "P123"

    def test_edit_slot_forbidden_status(self, api_client, auditor_user, slot):
        """Conferente NÃO pode editar se status não for AUDITING."""
        slot.status = Slot.Status.AVAILABLE
        slot.save()

        api_client.force_authenticate(user=auditor_user)
        url = reverse("cavaletes:slot-detail", args=[slot.id])
        data = {"quantity": 50}

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["detail"][0]) == str(messages.SLOT_INVALID_STATUS)
