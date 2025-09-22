import openpyxl
import io
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Cavalete, Slot
from .serializers import CavaleteSerializer, CavaleteAssignSerializer
from core.permissions import IsAdmin, IsManager, IsAuditor

User = get_user_model()

class CavaleteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Cavaletes.
    Permite CRUD, exportação, atribuição de usuário e histórico de ações.
    Mudança de status só via actions customizadas.
    """
    queryset = Cavalete.objects.all()
    serializer_class = CavaleteSerializer
    permission_classes = [IsManager|IsAdmin|IsAuditor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code', 'status']
    search_fields = ['code']
    ordering_fields = ['name', 'id']
    ordering = ['id']

    def _create_cavalete_history(self, instance, user, history_action, previous_data=None):
        """
        Cria um registro de histórico para o cavalete.
        Guarda o usuário, ação realizada e dados anteriores (se houver).
        """
        from inventory.models import CavaleteHistory
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
            return Cavalete.objects.filter(user=user).order_by('id')
        return Cavalete.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        """
        Cria um novo cavalete, gerando código e nome automáticos.
        Também cria os slots associados ao novo cavalete.
        """
        if Cavalete.objects.count() >= 30:
            return Response({'detail': 'Limite de 30 cavaletes atingido.'}, status=status.HTTP_400_BAD_REQUEST)
        last = Cavalete.objects.order_by('-id').first()
        last_num = 0
        if last and last.code.startswith('CAV'):
            try:
                last_num = int(last.code[3:])
            except ValueError:
                last_num = 0
        next_num = last_num + 1
        code = f'CAV{next_num:02d}'
        name = f'Cavalete {next_num:02d}'
        serializer = self.get_serializer(data={**request.data, 'code': code, 'name': name})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        cavalete = serializer.instance
        slots = [Slot(cavalete=cavalete, side=side, number=number) for side in ['A', 'B'] for number in range(1, 7)]
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

    @action(detail=False, methods=['get'], permission_classes=[IsManager|IsAdmin|IsAuditor])
    def product_stats(self, request):
        """
        Retorna estatísticas de produtos associados aos slots.
        """
        slots_with_products = Slot.objects.exclude(
            Q(product_code__isnull=True) | Q(product_code='')
        ).count()
        
        unique_products = Slot.objects.exclude(
            Q(product_code__isnull=True) | Q(product_code='')
        ).values('product_code').distinct().count()
        
        return Response({
            'slots_with_products': slots_with_products,
            'unique_products': unique_products
        })

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
