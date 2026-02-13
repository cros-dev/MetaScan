from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsAuditor, IsManager
from apps.core import messages as core_messages
from .models import Cavalete, Slot
from .serializers import CavaleteSerializer, SlotSerializer
from . import messages


class CavaleteViewSet(viewsets.ModelViewSet):
    """
    CRUD de Cavaletes.
    Gestores podem gerenciar tudo.
    Conferentes veem apenas os atribuídos a eles.
    """

    queryset = Cavalete.objects.all()
    serializer_class = CavaleteSerializer

    def get_permissions(self):
        """Define permissões baseadas na action."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsManager()]
        return [IsAuditor()]

    def get_queryset(self):
        """Filtra cavaletes por usuário se for conferente."""
        user = self.request.user
        qs = super().get_queryset()

        if user.is_authenticated and user.role == "AUDITOR":
            return qs.filter(user=user)

        return qs


class SlotViewSet(viewsets.ModelViewSet):
    """
    Gestão de slots. Conferentes editam produto/quantidade durante conferência.
    """

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAuditor]

    @action(detail=True, methods=["post"], url_path="start-confirmation")
    def start_confirmation(self, request, pk=None):
        """Inicia a conferência de um slot (Muda status para AUDITING)."""
        slot = self.get_object()

        if slot.status != Slot.Status.AVAILABLE:
            return Response(
                {"detail": messages.SLOT_INVALID_STATUS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        slot.status = Slot.Status.AUDITING
        slot.save()

        return Response(
            {"status": "AUDITING", "detail": messages.SLOT_CONFIRMATION_STARTED}
        )

    @action(detail=True, methods=["post"], url_path="finish-confirmation")
    def finish_confirmation(self, request, pk=None):
        """Finaliza a conferência de um slot (Muda status para COMPLETED)."""
        slot = self.get_object()

        if slot.status != Slot.Status.AUDITING:
            return Response(
                {"detail": messages.SLOT_INVALID_STATUS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        slot.status = Slot.Status.COMPLETED
        slot.save()

        return Response(
            {"status": "COMPLETED", "detail": messages.SLOT_CONFIRMATION_FINISHED}
        )
