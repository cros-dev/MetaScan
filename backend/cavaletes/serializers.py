from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Cavalete, Slot
from core.constants import ACTION_CHOICES

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para listagem básica de usuários.
    Retorna id, email, role e status ativo.
    """
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active']

class CavaleteSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Cavalete.
    Inclui slots relacionados e dados do usuário responsável.
    Bloqueia alteração de status via update padrão.
    """
    slots = serializers.SerializerMethodField()
    user = UserSummarySerializer(read_only=True)
    occupancy = serializers.SerializerMethodField()
    class Meta:
        model = Cavalete
        fields = ['id', 'code', 'name', 'user', 'status', 'slots', 'occupancy']

    def get_slots(self, obj):
        slots = obj.slots.all().order_by('number')
        return SlotSerializer(slots, many=True).data

    def get_occupancy(self, obj):
        slots = obj.slots.all()
        total = slots.count()
        occupied = slots.filter(status='completed').exclude(product_code__isnull=True).exclude(product_code='').count()
        percent = int(round((occupied / total) * 100)) if total > 0 else 0
        return f"{occupied}/{total} {percent}%"

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            raise serializers.ValidationError({"detail": "O status só pode ser alterado por ações específicas."})
        return super().update(instance, validated_data)

class CavaleteAssignSerializer(serializers.Serializer):
    """
    Serializer para atribuição em massa de cavaletes a um usuário.
    Recebe lista de IDs de cavaletes e opcionalmente o ID do usuário.
    """
    cavalete_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    user_id = serializers.IntegerField(required=False)

class SlotSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Slot.
    Inclui validações de produto, integração com Sankhya e restrição de update de status/produto.
    Só permite atualização de produto se status for 'auditing'.
    """
    action = serializers.CharField(write_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._product_description = None

    class Meta:
        model = Slot
        fields = ['id', 'cavalete', 'side', 'number', 'product_code', 'product_description', 'quantity', 'status', 'action']

    def validate_action(self, value):
        if value and value not in dict(ACTION_CHOICES):
            raise serializers.ValidationError({"detail": f"Valor inválido para 'action'. Aceitos: {', '.join(dict(ACTION_CHOICES))}", "code": "action_invalid"})
        return value

    def validate_product_code(self, value):
        from sankhya.services.sankhya_product import consult_sankhya_product
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if value and user and user.is_authenticated:
            result = consult_sankhya_product(value, user.id)
            if not result:
                raise serializers.ValidationError({"detail": "Produto não encontrado na Sankhya.", "code": "product_not_found"})
            self._product_description = result['description']
        return value

    def create(self, validated_data):
        description = getattr(self, '_product_description', None)
        validated_data.pop('action', None)
        if description:
            validated_data['product_description'] = description
        slot = super().create(validated_data)
        return slot

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            raise serializers.ValidationError({"detail": "O status só pode ser alterado por ações específicas."})
        campos_produto = {'product_code', 'product_description', 'quantity'}
        if any(campo in validated_data for campo in campos_produto):
            if instance.status != 'auditing':
                raise serializers.ValidationError({"detail": "Só é permitido atualizar produto quando o status for 'auditing'."})
            if 'product_code' in validated_data:
                instance.product_code = validated_data['product_code']
                if self._product_description:
                    instance.product_description = self._product_description
            if 'product_description' in validated_data:
                instance.product_description = validated_data['product_description']
            if 'quantity' in validated_data:
                instance.quantity = validated_data['quantity']
            instance.save()
            return instance
        return super().update(instance, validated_data)
