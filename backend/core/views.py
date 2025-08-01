import openpyxl
import io
import requests
import json
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from core.models import Cavalete, Slot, SlotHistory, CavaleteHistory
from core.permissions import IsAdmin, IsManager, IsAuditor
from core.serializers import (
    UserMeSerializer, CavaleteSerializer, SlotSerializer,
    SlotHistorySerializer, CavaleteHistorySerializer, CavaleteAssignSerializer, UserSummarySerializer
)
from core.services.sankhya_auth import sankhya_login
from core.services.sankhya_product import consult_sankhya_product, SankhyaAuthError

User = get_user_model()

class LoginView(APIView):
    """
    Endpoint de login integrado com Sankhya.
    Recebe credenciais, autentica no sistema externo e retorna JWT e dados do usuário.
    """
    authentication_classes = []
    permission_classes = []

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'detail': 'Email e senha obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        email = email.lower()
        bearer_token = sankhya_login(email, password)
        if not bearer_token:
            return Response({'detail': 'Usuário ou senha inválidos no Sankhya.'}, status=status.HTTP_401_UNAUTHORIZED)
        user, created = User.objects.get_or_create(email=email)
        user.set_password(password)
        user.sankhya_password = password
        user.save()
        refresh = RefreshToken.for_user(user)
        cache.set(f'sankhya_token_{user.id}', bearer_token, timeout=60*60)  # 1 hora
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
        })

class MeView(APIView):
    """
    Endpoint para retornar dados do usuário autenticado.
    Requer autenticação e retorna informações básicas do usuário logado.
    """
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

class TokenRefreshView(BaseTokenRefreshView):
    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({'detail': 'User not found or refresh token invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)

class CavaleteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Cavaletes.
    Permite CRUD, exportação, atribuição de usuário e histórico de ações.
    Mudança de status só via actions customizadas.
    """
    # noinspection PyUnresolvedReferences
    queryset = Cavalete.objects.all()
    serializer_class = CavaleteSerializer
    # Manager e admin podem tudo, auditor só vê os seus
    permission_classes = [IsManager|IsAdmin|IsAuditor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code', 'status']
    search_fields = ['code']
    ordering_fields = ['name', 'id']
    ordering = ['id']

    # noinspection PyMethodMayBeStatic
    def _create_cavalete_history(self, instance, user, history_action, previous_data=None):
        """
        Cria um registro de histórico para o cavalete.
        Guarda o usuário, ação realizada e dados anteriores (se houver).
        """
        # noinspection PyUnresolvedReferences
        CavaleteHistory.objects.create(
            cavalete=instance,
            user=user,
            action=history_action,
            previous_data=previous_data
        )

    def get_queryset(self):
        """
        Retorna o queryset de cavaletes visíveis para o usuário atual.
        Staff vê todos, usuário comum vê apenas os seus.
        """
        user = self.request.user
        if getattr(user, 'role', None) == 'auditor':
            # noinspection PyUnresolvedReferences
            return Cavalete.objects.filter(user=user).order_by('id')
        # noinspection PyUnresolvedReferences
        return Cavalete.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        """
        Cria um novo cavalete, gerando código e nome automáticos.
        Também cria os slots associados ao novo cavalete.
        """
        # noinspection PyUnresolvedReferences
        if Cavalete.objects.count() >= 30:
            return Response({'detail': 'Limite de 30 cavaletes atingido.'}, status=status.HTTP_400_BAD_REQUEST)
        # noinspection PyUnresolvedReferences
        ultimo = Cavalete.objects.order_by('-id').first()
        ultimo_num = 0
        if ultimo and ultimo.code.startswith('CAV'):
            try:
                ultimo_num = int(ultimo.code[3:])
            except ValueError:
                ultimo_num = 0
        novo_num = ultimo_num + 1
        code = f'CAV{novo_num:02d}'
        name = f'Cavalete {novo_num:02d}'
        serializer = self.get_serializer(data={**request.data, 'code': code, 'name': name})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        cavalete = serializer.instance
        slots = [Slot(cavalete=cavalete, side=side, number=number) for side in ['A', 'B'] for number in range(1, 7)]
        # noinspection PyUnresolvedReferences
        Slot.objects.bulk_create(slots)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(cavalete).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def export(self, request):
        """
        Exporta os dados dos cavaletes e seus slots em formato Excel (.xlsx).
        Permite filtrar por IDs ou nomes de cavaletes.
        Apenas para administradores.
        """
        ids = request.query_params.getlist('cavalete_id')
        names = request.query_params.getlist('cavalete_name')
        # noinspection PyUnresolvedReferences
        qs = Cavalete.objects.prefetch_related('slots').order_by('-name')
        if ids and names:
            qs = qs.filter(Q(id__in=ids) | Q(name__in=names))
        elif ids:
            qs = qs.filter(id__in=ids)
        elif names:
            qs = qs.filter(name__in=names)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Cavaletes"
        ws.append([
            'Name', 'Side', 'Number', 'Product Code', 'Product Description', 'Quantity'
        ])
        for cav in qs.all():
            slots = list(cav.slots.all())
            slots_dict = {(slot.side, slot.number): slot for slot in slots}
            for side in ['A', 'B']:
                for number in range(1, 7):
                    slot = slots_dict.get((side, number))
                    if slot:
                        ws.append([
                            cav.name,
                            side,
                            number,
                            slot.product_code if slot.product_code else '',
                            slot.product_description if slot.product_description else '',
                            slot.quantity if slot.quantity is not None else 0
                        ])
                    else:
                        ws.append([
                            cav.name,
                            side,
                            number,
                            '', '', 0
                        ])
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=cavaletes.xlsx'
        return response

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def assign_user(self, request, **kwargs):
        """
        Atribui ou libera um usuário responsável por um cavalete específico.
        Altera o status do cavalete para 'assigned' ou 'available'.
        Apenas para administradores.
        """
        cavalete = self.get_object()
        user_id = request.data.get('user_id')
        previous_data = {
            'name': cavalete.name,
            'user': cavalete.user.id if cavalete.user else None,
            'status': cavalete.status
        }
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                cavalete.user = user
                cavalete.status = 'assigned'
                cavalete.save()
                self._create_cavalete_history(cavalete, request.user, 'assigned', previous_data)
                return Response({'detail': 'Usuário atribuído com sucesso.'})
            except User.DoesNotExist:
                return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cavalete.user = None
            cavalete.status = 'available'
            cavalete.save()
            self._create_cavalete_history(cavalete, request.user, 'released', previous_data)
            return Response({'detail': 'Cavalete liberado com sucesso.'})

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser], serializer_class=CavaleteAssignSerializer)
    def assign(self, request, **kwargs):
        """
        Atribui em massa um usuário a vários cavaletes.
        Altera o status dos cavaletes para 'assigned' ou 'available'.
        Apenas para administradores.
        """
        ids = request.data.get('cavalete_ids', [])
        user_id = request.data.get('user_id')
        user = None
        if not ids:
            return Response({'detail': 'Informe uma lista de IDs de cavaletes.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        # noinspection PyUnresolvedReferences
        updated = Cavalete.objects.filter(id__in=ids)
        for cav in updated:
            previous_data = {
                'name': cav.name,
                'user': cav.user.id if cav.user else None,
                'status': cav.status
            }
            history_action = 'assigned' if user else 'released'
            if user:
                cav.user = user
                cav.status = 'assigned'
            else:
                cav.user = None
                cav.status = 'available'
            cav.save()
            self._create_cavalete_history(cav, request.user, history_action, previous_data)
        return Response({
            'detail': 'Atribuição em massa realizada com sucesso.',
            'cavalete_ids': ids,
            'user': user_id if user else None
        })

    def perform_create(self, serializer):
        """
        Salva o cavalete e registra o histórico de criação.
        """
        instance = serializer.save()
        self._create_cavalete_history(instance, self.request.user, 'created')

    def perform_update(self, serializer):
        """
        Atualiza o cavalete e registra o histórico de edição.
        Alteração de status deve ser feita apenas via actions customizadas.
        """
        instance = self.get_object()
        previous_data = {
            'name': instance.name,
            'user': instance.user.id if instance.user else None
        }
        updated_instance = serializer.save()
        self._create_cavalete_history(updated_instance, self.request.user, 'edited', previous_data)

    def perform_destroy(self, instance):
        """
        Remove o cavalete e registra o histórico de deleção.
        """
        previous_data = {
            'name': instance.name,
            'user': instance.user.id if instance.user else None
        }
        self._create_cavalete_history(instance, self.request.user, 'deleted', previous_data)
        instance.delete()

class SlotViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Slots.
    Permite CRUD, histórico, transições de status via actions e edição de produto apenas em conferência.
    """
    # noinspection PyUnresolvedReferences
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    # Manager, auditor e admin podem acessar, mas auditor só vê/edita seus slots
    permission_classes = [IsManager|IsAdmin|IsAuditor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'cavalete': ['exact'],
        'side': ['exact'],
        'number': ['exact'],
    }
    ordering = ['number']

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'auditor':
            # noinspection PyUnresolvedReferences
            return Slot.objects.filter(cavalete__user=user).order_by('number')
        # noinspection PyUnresolvedReferences
        return Slot.objects.all().order_by('number')

    # noinspection PyMethodMayBeStatic
    def _create_slot_history(self, slot, user, slot_action):
        """
        Cria um registro de histórico para o slot.
        Guarda o usuário, ação realizada e dados do produto.
        """
        # noinspection PyUnresolvedReferences
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
        
        # Filtra slots do cavalete específico e disponíveis
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
        
        # Filtra slots do cavalete específico em auditing
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
        
        # Filtra slots do cavalete específico concluídos
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
        
        # Filtra slots do cavalete específico aguardando aprovação
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
    # noinspection PyUnresolvedReferences
    queryset = CavaleteHistory.objects.all().order_by('-timestamp')
    serializer_class = CavaleteHistorySerializer
    permission_classes = [IsManager|IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'user': ['exact'],
        'cavalete': ['exact'],
        'action': ['exact'],
        'timestamp': ['gte', 'lte'],
    }
    search_fields = ['action']
    ordering_fields = ['timestamp', 'user', 'cavalete', 'action']

class ProductConsultView(APIView):
    """
    Endpoint para consultar produtos na Sankhya.
    Requer autenticação e retorna dados do produto consultado pelo código.
    """
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request, code):
        user_id = request.user.id
        try:
            product = consult_sankhya_product(code, user_id)
        except SankhyaAuthError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except requests.RequestException:
            return Response({"detail": "Erro de conexão com a Sankhya."}, status=status.HTTP_502_BAD_GATEWAY)
        except json.JSONDecodeError:
            return Response({"detail": "Erro ao processar resposta da Sankhya (JSON inválido)."}, status=status.HTTP_502_BAD_GATEWAY)
        if product:
            return Response(product)
        return Response({"detail": "Produto não encontrado na Sankhya."}, status=status.HTTP_404_NOT_FOUND)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de listagem de usuários (apenas admin).
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSummarySerializer
    permission_classes = [IsAdmin]
