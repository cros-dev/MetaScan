from rest_framework import viewsets, mixins
from apps.core.permissions import IsManager
from .models import CavaleteHistory, SlotHistory
from .serializers import CavaleteHistorySerializer, SlotHistorySerializer


class CavaleteHistoryViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Lista histórico de ações em cavaletes.
    Apenas leitura.
    Acessível por Gestores.
    """

    queryset = CavaleteHistory.objects.all()
    serializer_class = CavaleteHistorySerializer
    permission_classes = [IsManager]
    filterset_fields = ["cavalete", "user", "action"]


class SlotHistoryViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Lista histórico de ações em slots.
    Apenas leitura.
    Acessível por Gestores.
    """

    queryset = SlotHistory.objects.all()
    serializer_class = SlotHistorySerializer
    permission_classes = [IsManager]
    filterset_fields = ["slot", "user", "action", "slot__cavalete"]
