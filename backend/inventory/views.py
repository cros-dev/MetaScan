from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.apps import apps

from .models import SlotHistory, CavaleteHistory
from .serializers import SlotHistorySerializer, CavaleteHistorySerializer
from core.permissions import IsAdmin, IsManager, IsAuditor

User = get_user_model()

class SlotViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Slots.
    Permite CRUD, histórico, transições de status via actions e edição de produto apenas em conferência.
    """
    
    def get_queryset(self):
        Slot = apps.get_model('cavaletes', 'Slot')
        user = self.request.user
        if getattr(user, 'role', None) == 'auditor':
            return Slot.objects.filter(cavalete__user=user).order_by('number')
        return Slot.objects.all().order_by('number')
    
    def get_serializer_class(self):
        from cavaletes.serializers import SlotSerializer
        return SlotSerializer
    permission_classes = [IsManager|IsAdmin|IsAuditor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'cavalete': ['exact'],
        'side': ['exact'],
        'number': ['exact'],
    }
    ordering = ['number']



    def _create_slot_history(self, slot, user, slot_action):
        """
        Cria um registro de histórico para o slot.
        Guarda o usuário, ação realizada e dados do produto.
        """
        SlotHistory.objects.create(
            slot=slot,
            user=user,
            product_code=slot.product_code,
            product_description=slot.product_description,
            quantity=slot.quantity,
            action=slot_action
        )

    def _update_slot_status(self, slot, expected_status, new_status, user, slot_action, success_message, error_message):
        """
        Atualiza o status do slot, validando o status atual antes da transição.
        Registra histórico e retorna resposta adequada.
        """
        if slot.status != expected_status:
            return Response({'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
        slot.status = new_status
        slot.save()
        self._create_slot_history(slot, user, slot_action)
        return Response({'detail': success_message})

    def perform_create(self, serializer):
        """
        Salva o slot e registra o histórico de criação.
        """
        slot = serializer.save()
        user = self.request.user
        slot_action = self.request.data.get('action', 'confirmation')
        self._create_slot_history(slot, user, slot_action)

    def perform_update(self, serializer):
        """
        Atualiza o slot e registra o histórico de edição.
        Alteração de status deve ser feita apenas via actions customizadas.
        """
        slot = serializer.save()
        user = self.request.user
        slot_action = self.request.data.get('action', None) or 'confirmation'
        self._create_slot_history(slot, user, slot_action)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def start_confirmation(self, request, **kwargs):
        """
        Inicia o processo de conferência do slot.
        Só pode ser chamado se o slot estiver 'available'.
        Altera status para 'auditing'.
        Apenas para administradores.
        """
        slot = self.get_object()
        return self._update_slot_status(
            slot, 'available', 'auditing', request.user,
            'start_confirmation',
            'Conferência iniciada com sucesso.',
            'Slot não está disponível para iniciar conferência.'
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuditor|IsAdmin])
    def finish_confirmation(self, request, **kwargs):
        """
        Finaliza a conferência do slot pelo conferente ou admin (exceção).
        Só pode ser chamado se o slot estiver 'auditing'.
        Altera status para 'awaiting_approval'.
        """
        slot = self.get_object()
        return self._update_slot_status(
            slot, 'auditing', 'awaiting_approval', request.user,
            'finish_confirmation',
            'Conferência finalizada. Aguardando aprovação do gestor.',
            'Slot não está em conferência.'
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve_confirmation(self, request, **kwargs):
        """
        Aprova a conferência do slot (gestor).
        Só pode ser chamado se o slot estiver 'awaiting_approval'.
        Altera status para 'completed'.
        Apenas para administradores.
        """
        slot = self.get_object()
        return self._update_slot_status(
            slot, 'awaiting_approval', 'completed', request.user,
            'approve_confirmation',
            'Conferência concluída com sucesso.',
            'Slot não está aguardando conclusão.'
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def return_confirmation(self, request, **kwargs):
        """
        Devolve o slot para nova conferência pelo conferente.
        Só pode ser chamado se o slot estiver 'awaiting_approval'.
        Altera status para 'auditing'.
        Apenas para administradores.
        """
        slot = self.get_object()
        return self._update_slot_status(
            slot, 'awaiting_approval', 'auditing', request.user,
            'return_confirmation',
            'Conferência devolvida ao conferente.',
            'Slot não está aguardando conclusão.'
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reopen_confirmation(self, request, **kwargs):
        """
        Reabre a conferência de um slot já concluído.
        Só pode ser chamado se o slot estiver 'completed'.
        Altera status para 'auditing'.
        Apenas para administradores.
        """
        slot = self.get_object()
        return self._update_slot_status(
            slot, 'completed', 'auditing', request.user,
            'reopen_confirmation',
            'Conferência reaberta. Slot disponível para edição pelo conferente.',
            'Só é possível reabrir slots concluídos.'
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def start_all(self, request):
        """
        Inicia conferência em todos os slots disponíveis (status 'available') de um cavalete específico.
        Apenas para administradores.
        """
        cavalete_id = request.data.get('cavalete_id')
        
        if not cavalete_id:
            return Response({'detail': 'cavalete_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        available_slots = self.get_queryset().filter(
            cavalete_id=cavalete_id,
            status='available'
        )
        
        if not available_slots.exists():
            return Response({'detail': 'Nenhum slot disponível para iniciar conferência neste cavalete.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = 0
        for slot in available_slots:
            slot.status = 'auditing'
            slot.save()
            self._create_slot_history(slot, request.user, 'start_confirmation')
            updated_count += 1
        
        return Response({
            'detail': f'Conferência iniciada em {updated_count} slots do cavalete com sucesso.',
            'updated_count': updated_count,
            'cavalete_id': cavalete_id
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuditor|IsAdmin])
    def finish_all(self, request):
        """
        Encerra conferência em todos os slots em auditing de um cavalete específico.
        Altera status para 'awaiting_approval'.
        Apenas para conferentes e administradores.
        """
        cavalete_id = request.data.get('cavalete_id')
        
        if not cavalete_id:
            return Response({'detail': 'cavalete_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        auditing_slots = self.get_queryset().filter(
            cavalete_id=cavalete_id,
            status='auditing'
        )
        
        if not auditing_slots.exists():
            return Response({'detail': 'Nenhum slot em conferência neste cavalete.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = 0
        for slot in auditing_slots:
            slot.status = 'awaiting_approval'
            slot.save()
            self._create_slot_history(slot, request.user, 'finish_confirmation')
            updated_count += 1
        
        return Response({
            'detail': f'Conferência encerrada em {updated_count} slots do cavalete. Aguardando aprovação do gestor.',
            'updated_count': updated_count,
            'cavalete_id': cavalete_id
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def reopen_all(self, request):
        """
        Reabre conferência em todos os slots concluídos (status 'completed') de um cavalete específico.
        Altera status para 'auditing'.
        Apenas para administradores.
        """
        cavalete_id = request.data.get('cavalete_id')
        
        if not cavalete_id:
            return Response({'detail': 'cavalete_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        completed_slots = self.get_queryset().filter(
            cavalete_id=cavalete_id,
            status='completed'
        )
        
        if not completed_slots.exists():
            return Response({'detail': 'Nenhum slot concluído neste cavalete.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = 0
        for slot in completed_slots:
            slot.status = 'auditing'
            slot.save()
            self._create_slot_history(slot, request.user, 'reopen_confirmation')
            updated_count += 1
        
        return Response({
            'detail': f'Conferência reaberta em {updated_count} slots do cavalete. Slots disponíveis para edição pelo conferente.',
            'updated_count': updated_count,
            'cavalete_id': cavalete_id
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def approve_all(self, request):
        """
        Aprova conferência em todos os slots aguardando aprovação (status 'awaiting_approval') de um cavalete específico.
        Altera status para 'completed'.
        Apenas para administradores.
        """
        cavalete_id = request.data.get('cavalete_id')
        
        if not cavalete_id:
            return Response({'detail': 'cavalete_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        awaiting_slots = self.get_queryset().filter(
            cavalete_id=cavalete_id,
            status='awaiting_approval'
        )
        
        if not awaiting_slots.exists():
            return Response({'detail': 'Nenhum slot aguardando aprovação neste cavalete.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = 0
        for slot in awaiting_slots:
            slot.status = 'completed'
            slot.save()
            self._create_slot_history(slot, request.user, 'approve_confirmation')
            updated_count += 1
        
        return Response({
            'detail': f'Conferência aprovada em {updated_count} slots do cavalete com sucesso.',
            'updated_count': updated_count,
            'cavalete_id': cavalete_id
        })

class SlotHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para histórico de Slots.
    Permite consulta filtrada e ordenada do histórico de alterações dos slots.
    """
    queryset = SlotHistory.objects.all().order_by('-timestamp')
    serializer_class = SlotHistorySerializer
    permission_classes = [IsManager|IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'user': ['exact'],
        'slot': ['exact'],
        'product_code': ['exact'],
        'timestamp': ['gte', 'lte'],
    }
    search_fields = ['product_description']
    ordering_fields = ['timestamp', 'user', 'slot', 'product_code']

class CavaleteHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para histórico de Cavaletes.
    Permite consulta filtrada e ordenada do histórico de alterações dos cavaletes.
    """
    queryset = CavaleteHistory.objects.all().order_by('-timestamp')
    serializer_class = CavaleteHistorySerializer
    permission_classes = [IsManager|IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'user': ['exact'],
        'action': ['exact'],
        'timestamp': ['gte', 'lte'],
    }
    search_fields = ['action']
    ordering_fields = ['timestamp', 'user', 'cavalete', 'action']
