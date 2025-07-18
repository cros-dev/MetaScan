from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.services.sankhya_auth import sankhya_login
from django.contrib.auth import get_user_model
from core.serializers import MeSerializer
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'detail': 'Email e senha obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        email = email.lower()
        bearer_token = sankhya_login(email, password)
        if not bearer_token:
            return Response({'detail': 'Usuário ou senha inválidos no Sankhya.'}, status=status.HTTP_401_UNAUTHORIZED)
        user, created = User.objects.get_or_create(email=email)
        user.set_password(password)
        user.sankhya_password = password
        user.save()
        refresh = RefreshToken.for_user(user)
        cache.set(f'sankhya_token_{user.id}', bearer_token, timeout=60*60)  # 1 hora
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
