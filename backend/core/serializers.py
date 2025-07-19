from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Cavalete, Slot, SlotHistory, CavaleteHistory

User = get_user_model()

class UserMeSerializer(serializers.ModelSerializer):
    """
    Serializer para o endpoint /me/ (usuário autenticado).
    """
    email = serializers.EmailField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser']

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para listagem básica de usuários.
    """
    class Meta:
        model = User
        fields = ['id', 'email']

class CavaleteSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Cavalete, incluindo slots e usuário.
    """
    slots = serializers.SerializerMethodField()
    user = UserSummarySerializer(read_only=True)
    class Meta:
        model = Cavalete
        fields = ['id', 'code', 'name', 'user', 'status', 'slots']

    # noinspection PyMethodMayBeStatic
    def get_slots(self, obj):
        slots = obj.slots.all()
        return SlotSerializer(slots, many=True).data

class SlotSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Slot, incluindo validações e integração com Sankhya.
    """
    action = serializers.CharField(write_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._product_description = None

    class Meta:
        model = Slot
        fields = ['id', 'cavalete', 'side', 'number', 'product_code', 'product_description', 'quantity', 'status', 'action']

    # noinspection PyMethodMayBeStatic
    def validate_action(self, value):
        from core.models import ACTION_CHOICES
        if value and value not in dict(ACTION_CHOICES):
            raise serializers.ValidationError({"detail": f"Valor inválido para 'action'. Aceitos: {', '.join(dict(ACTION_CHOICES))}", "code": "action_invalid"})
        return value

    def validate_product_code(self, value):
        from core.services.sankhya_product import consult_sankhya_product
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        # _product_description é usado como cache temporário para o valor retornado da Sankhya
        if value and user and user.is_authenticated:
            result = consult_sankhya_product(value, user.id)
            if not result:
                raise serializers.ValidationError({"detail": "Produto não encontrado na Sankhya.", "code": "product_not_found"})
            self._product_description = result['description']
        return value

    def create(self, validated_data):
        description = getattr(self, '_product_description', None)
        validated_data.pop('action', None)  # Remove o campo action, não usado aqui
        if description:
            validated_data['product_description'] = description
        slot = super().create(validated_data)
        return slot

    def update(self, instance, validated_data):
        validated_data.pop('action', None)  # Remove o campo action, não usado aqui
        description = getattr(self, '_product_description', None)
        if description:
            validated_data['product_description'] = description
        slot = super().update(instance, validated_data)
        return slot

class SlotHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para histórico de conferência de slots.
    """
    user = serializers.EmailField(source='user.email', read_only=True)
    cavalete_id = serializers.SerializerMethodField()
    cavalete_name = serializers.SerializerMethodField()
    class Meta:
        model = SlotHistory
        fields = ['id', 'cavalete_id', 'cavalete_name', 'slot', 'user', 'timestamp', 'product_code', 'product_description', 'quantity', 'action']

    # noinspection PyMethodMayBeStatic
    def get_cavalete_id(self, obj):
        return obj.slot.cavalete.id if obj.slot and obj.slot.cavalete else None

    # noinspection PyMethodMayBeStatic
    def get_cavalete_name(self, obj):
        return obj.slot.cavalete.name if obj.slot and obj.slot.cavalete else None

class CavaleteHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para histórico de ações em Cavalete.
    """
    user = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = CavaleteHistory
        fields = ['id', 'cavalete', 'user', 'timestamp', 'action', 'previous_data']

class CavaleteAssignSerializer(serializers.Serializer):
    """
    Serializer para atribuição em massa de cavaletes a um usuário.
    """
    cavalete_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    user_id = serializers.IntegerField(required=False)
