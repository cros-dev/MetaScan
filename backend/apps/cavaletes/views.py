from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.permissions import IsAuditor, IsManager
from apps.core import messages as core_messages
from apps.inventory.models import Action
from apps.inventory.services import log_cavalete_action, log_slot_action, create_cavalete_structure
from .models import Cavalete, Slot
from .serializers import CavaleteSerializer, SlotSerializer
from . import messages

User = get_user_model()


class CavaleteViewSet(viewsets.ModelViewSet):
    """
    CRUD de Cavaletes.
    Gestores podem gerenciar tudo.
    Conferentes veem apenas os atribuídos a eles.
    Filtros: ?status=AVAILABLE. Busca: ?search=CAV-001 (por código).
    """

    queryset = Cavalete.objects.all()
    serializer_class = CavaleteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["code"]

    def get_permissions(self):
        """Define permissões baseadas na action."""
        if self.action in ["create", "update", "partial_update", "destroy", "assign_user"]:
            return [IsManager()]
        return [IsAuditor()]

    def get_queryset(self):
        """Filtra cavaletes por usuário se for conferente."""
        user = self.request.user
        qs = super().get_queryset()

        if user.is_authenticated and user.role == "AUDITOR":
            return qs.filter(user=user)

        return qs

    def perform_create(self, serializer):
        """Salva e registra log de criação."""
        with transaction.atomic():
            structure_data = serializer.validated_data.pop("structure", None)
            
            instance = serializer.save()
            log_cavalete_action(instance, self.request.user, Action.CREATE)

            if structure_data:
                create_cavalete_structure(
                    instance,
                    slots_a=structure_data.get("slots_a", 0),
                    slots_b=structure_data.get("slots_b", 0),
                )

    def perform_update(self, serializer):
        """Salva e registra log de atualização."""
        with transaction.atomic():
            instance = serializer.save()
            log_cavalete_action(instance, self.request.user, Action.UPDATE)

    def perform_destroy(self, instance):
        """Deleta e registra log de exclusão."""
        with transaction.atomic():
            log_cavalete_action(
                instance,
                self.request.user,
                Action.DELETE,
                description=f"Cavalete {instance.code} excluído",
            )
            instance.delete()

    @action(detail=True, methods=["post"], url_path="assign-user")
    def assign_user(self, request, pk=None):
        """Atribui um conferente ao cavalete. Apenas gestores."""
        cavalete = self.get_object()
        user_id = request.data.get("user_id")
        if user_id is None:
            return Response(
                {"detail": "user_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": str(core_messages.USER_NOT_FOUND)},
                status=status.HTTP_404_NOT_FOUND,
            )
        with transaction.atomic():
            cavalete.user = user
            cavalete.save()
            log_cavalete_action(
                cavalete,
                request.user,
                Action.ASSIGN,
                description=f"Atribuído a {user.username}",
            )
        serializer = self.get_serializer(cavalete)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SlotViewSet(viewsets.ModelViewSet):
    """
    Gestão de slots. Conferentes editam produto/quantidade durante conferência.
    """

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAuditor]

    def perform_update(self, serializer):
        """Salva e registra log detalhado de atualização."""
        with transaction.atomic():
            instance = serializer.instance
            old_data = {
                "product_code": instance.product_code,
                "quantity": instance.quantity,
            }

            updated_instance = serializer.save()

            new_data = {
                "product_code": updated_instance.product_code,
                "quantity": updated_instance.quantity,
            }

            log_slot_action(
                updated_instance,
                self.request.user,
                Action.UPDATE,
                old_data=old_data,
                new_data=new_data,
            )

    @action(detail=True, methods=["post"], url_path="start-confirmation")
    def start_confirmation(self, request, pk=None):
        """Inicia a conferência de um slot (Muda status para AUDITING)."""
        with transaction.atomic():
            slot = self.get_object()

            if slot.status != Slot.Status.AVAILABLE:
                return Response(
                    {"detail": messages.SLOT_INVALID_STATUS},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            slot.status = Slot.Status.AUDITING
            slot.save()

            log_slot_action(
                slot,
                request.user,
                Action.START_AUDIT,
                description="Conferência iniciada",
            )

        return Response(
            {"status": "AUDITING", "detail": messages.SLOT_CONFIRMATION_STARTED}
        )

    @action(detail=True, methods=["post"], url_path="finish-confirmation")
    def finish_confirmation(self, request, pk=None):
        """Finaliza a conferência de um slot (Muda status para COMPLETED)."""
        with transaction.atomic():
            slot = self.get_object()

            if slot.status != Slot.Status.AUDITING:
                return Response(
                    {"detail": messages.SLOT_INVALID_STATUS},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            slot.status = Slot.Status.COMPLETED
            slot.save()

            log_slot_action(
                slot,
                request.user,
                Action.FINISH_AUDIT,
                description="Conferência finalizada",
            )

        return Response(
            {"status": "COMPLETED", "detail": messages.SLOT_CONFIRMATION_FINISHED}
        )
