from rest_framework import serializers
from .models import CavaleteHistory, SlotHistory


class CavaleteHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = CavaleteHistory
        fields = [
            "id",
            "cavalete",
            "user",
            "user_name",
            "action",
            "action_display",
            "description",
            "timestamp",
        ]


class SlotHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = SlotHistory
        fields = [
            "id",
            "slot",
            "user",
            "user_name",
            "action",
            "action_display",
            "old_product_code",
            "new_product_code",
            "old_quantity",
            "new_quantity",
            "description",
            "timestamp",
        ]
