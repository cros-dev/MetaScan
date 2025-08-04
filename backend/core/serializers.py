from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Cavalete, Slot, SlotHistory, CavaleteHistory

User = get_user_model()

class UserMeSerializer(serializers.ModelSerializer):
    """
    Serializer para o endpoint /me/ (usuário autenticado).
    Retorna informações básicas do usuário logado.
    """
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para listagem básica de usuários.
    Retorna id, email, role e status ativo.
    """
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active']

class UserFullSerializer(serializers.ModelSerializer):
    """
    Serializer completo para criação e atualização de usuários.
    Permite definir email, role e senha.
    """
    password = serializers.CharField(write_only=True, required=False, min_length=6)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=User.role.field.choices, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def validate_email(self, value):
        """
        Valida se o email é único.
        """
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(id=user.id if user.id else None).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
    
    def validate_role(self, value):
        """
        Impede alteração da role do primeiro superuser criado.
        """
        if self.instance and self.instance.is_superuser:
            first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
            if first_superuser and self.instance.id == first_superuser.id:
                if value != self.instance.role:
                    raise serializers.ValidationError("Não é possível alterar a role do administrador padrão.")
        return value
    
    def validate_is_active(self, value):
        """
        Impede desativação do primeiro superuser criado.
        """
        if self.instance and self.instance.is_superuser and not value:
            first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
            if first_superuser and self.instance.id == first_superuser.id:
                raise serializers.ValidationError("Não é possível desativar o administrador padrão.")
        return value
    
    def create(self, validated_data):
        """
        Cria usuário com senha criptografada.
        """
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Atualiza usuário, tratando senha separadamente.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

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

    # noinspection PyMethodMayBeStatic
    def get_slots(self, obj):
        slots = obj.slots.all().order_by('number')
        return SlotSerializer(slots, many=True).data

    # noinspection PyMethodMayBeStatic
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
                raise serializers.ValidationError({"detail": f"Só é permitido atualizar produto quando o slot está em conferência (auditing). Status atual: '{instance.status}'."})
        validated_data.pop('action', None)
        description = getattr(self, '_product_description', None)
        if description:
            validated_data['product_description'] = description
        slot = super().update(instance, validated_data)
        return slot

class SlotHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para histórico de conferência de slots.
    Retorna dados do usuário, cavalete e detalhes da ação.
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
    Retorna dados do usuário, cavalete e detalhes da ação.
    """
    user = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = CavaleteHistory
        fields = ['id', 'cavalete', 'user', 'timestamp', 'action', 'previous_data']

