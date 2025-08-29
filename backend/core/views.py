from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from core.permissions import IsAdmin
from core.serializers import (
    UserMeSerializer, UserSummarySerializer, UserFullSerializer
)
from sankhya.services.sankhya_auth import sankhya_login

User = get_user_model()

class LoginView(APIView):
    """
    Endpoint de login integrado com Sankhya.
    Recebe credenciais, autentica no sistema externo e retorna JWT e dados do usuário.
    """
    authentication_classes = []
    permission_classes = []

    def _handle_sankhya_login(self, user, password, bearer_token):
        """
        Processa login Sankhya bem-sucedido.
        Atualiza senha do usuário e retorna resposta com tokens.
        """
        user.set_password(password)
        user.sankhya_password = password
        user.save()
        
        refresh = RefreshToken.for_user(user)
        cache.set(f'sankhya_token_{user.id}', bearer_token, timeout=60*60)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role,
            'user_id': user.id,
            'email': user.email,
            'login_type': 'sankhya'
        })

    def post(self, request):
        """
        Autentica usuário no sistema.
        - Admin: Tenta login local primeiro, depois Sankhya se falhar
        - Usuários operacionais: Login Sankhya
        Só permite login se o usuário foi previamente criado pelo admin.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'detail': 'Email e senha obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = email.lower()
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Usuário não cadastrado no sistema. Entre em contato com o administrador.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'detail': 'Usuário desativado. Entre em contato com o administrador.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role == 'admin':
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': user.role,
                    'user_id': user.id,
                    'email': user.email,
                    'login_type': 'local'
                })
            
            bearer_token = sankhya_login(email, password)
            if bearer_token:
                return self._handle_sankhya_login(user, password, bearer_token)
            
            return Response({'detail': 'Senha incorreta.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        bearer_token = sankhya_login(email, password)
        if not bearer_token:
            return Response({'detail': 'Usuário ou senha inválidos no Sankhya.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return self._handle_sankhya_login(user, password, bearer_token)

class MeView(APIView):
    """
    Endpoint para retornar dados do usuário autenticado.
    Requer autenticação e retorna informações básicas do usuário logado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

class TokenRefreshView(BaseTokenRefreshView):
    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({'detail': 'User not found or refresh token invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de usuários.
    Permite CRUD, filtros e busca. Apenas para administradores.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSummarySerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email']
    ordering_fields = ['email', 'role', 'date_joined']
    ordering = ['id']

    def get_serializer_class(self):
        """
        Usa serializer completo para create/update, resumido para list/retrieve.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return UserFullSerializer
        return UserSummarySerializer

    def perform_create(self, serializer):
        """
        Cria usuário com senha criptografada.
        """
        user = serializer.save()
        if not user.password:
            user.set_password('123456')
            user.save()

    def perform_update(self, serializer):
        """
        Atualiza usuário, mantendo senha se não fornecida.
        """
        user = serializer.save()
        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
            user.save()

    def perform_destroy(self, instance):
        """
        Remove o usuário permanentemente do sistema.
        Impede remoção do primeiro superuser.
        """
        first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
        if first_superuser and instance.id == first_superuser.id:
            raise serializers.ValidationError("Não é possível remover o administrador padrão.")
        
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def deactivate(self, request, **kwargs):
        """
        Desativa um usuário temporariamente (soft delete).
        O usuário não poderá fazer login, mas permanece no sistema.
        Apenas para administradores.
        """
        user = self.get_object()
        first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
        if first_superuser and user.id == first_superuser.id:
            return Response({'detail': 'Não é possível desativar o administrador padrão.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            return Response({'detail': 'Usuário já está desativado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()
        
        return Response({
            'detail': f'Usuário {user.email} desativado com sucesso.',
            'user_id': user.id,
            'email': user.email,
            'is_active': False
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reactivate(self, request, **kwargs):
        """
        Reativa um usuário desativado.
        Apenas para administradores.
        """
        user = self.get_object()
        first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
        if first_superuser and user.id == first_superuser.id:
            return Response({'detail': 'Administrador padrão não pode ser reativado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active:
            return Response({'detail': 'Usuário já está ativo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = True
        user.save()
        
        return Response({
            'detail': f'Usuário {user.email} reativado com sucesso.',
            'user_id': user.id,
            'email': user.email,
            'is_active': True
        })


