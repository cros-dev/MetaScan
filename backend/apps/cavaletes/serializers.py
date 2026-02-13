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

    class Meta:
        model = Cavalete
        fields = [
            "id",
            "code",
            "name",
            "status",
            "user",
            "user_name",
            "slots",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
