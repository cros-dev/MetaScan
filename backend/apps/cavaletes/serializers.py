from rest_framework import serializers
from .models import Cavalete, Slot
from apps.core import messages as core_messages
from . import messages


class SlotSerializer(serializers.ModelSerializer):
    """
    Serializer para o Slot.
    """

    class Meta:
        model = Slot
        fields = [
            "id",
            "side",
            "number",
            "product_code",
            "product_description",
            "quantity",
            "status",
        ]
        read_only_fields = ["id", "status"]

    def validate(self, data):
        """
        Garante que edição de produto/quantidade só ocorra se status=AUDITING.
        """
        if not self.instance:
            return data

        if self.instance.status != Slot.Status.AUDITING:
            protected_fields = ["product_code", "product_description", "quantity"]
            for field in protected_fields:
                if field in data and data[field] != getattr(self.instance, field):
                    raise serializers.ValidationError(
                        {"detail": messages.SLOT_INVALID_STATUS}
                    )

        return data


class CavaleteSerializer(serializers.ModelSerializer):
    """
    Serializer completo do Cavalete, incluindo slots aninhados.
    """

    slots = SlotSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    structure = serializers.JSONField(
        write_only=True,
        required=False,
        help_text="Estrutura inicial: {'slots_a': int, 'slots_b': int}",
    )

    class Meta:
        model = Cavalete
        fields = [
            "id",
            "code",
            "type",
            "status",
            "user",
            "user_name",
            "slots",
            "structure",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_structure(self, value):
        """Valida se a estrutura possui os campos necessários."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Deve ser um objeto JSON.")
        
        slots_a = value.get("slots_a", 0)
        slots_b = value.get("slots_b", 0)

        if not isinstance(slots_a, int) or not isinstance(slots_b, int):
            raise serializers.ValidationError("slots_a e slots_b devem ser inteiros.")
        
        if slots_a < 0 or slots_b < 0:
            raise serializers.ValidationError("Quantidade de slots não pode ser negativa.")
            
        return value
