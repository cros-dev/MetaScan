"""
Views para o app accounts.

Views genéricas para gerenciamento de usuários, compatíveis com JWT.
"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View para obter e atualizar perfil do usuário autenticado.

    GET: Retorna dados do usuário autenticado
    PUT/PATCH: Atualiza dados do usuário (email, first_name, last_name)
    Requer autenticação JWT.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserDetailView(generics.RetrieveAPIView):
    """
    View para obter detalhes de um usuário por ID.

    GET: Retorna dados públicos do usuário
    Requer autenticação JWT.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
