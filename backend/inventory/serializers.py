from rest_framework import serializers
from .models import SlotHistory, CavaleteHistory

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

    def get_cavalete_id(self, obj):
        return obj.slot.cavalete.id if obj.slot and obj.slot.cavalete else None

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
