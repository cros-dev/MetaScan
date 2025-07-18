from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class MeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser']