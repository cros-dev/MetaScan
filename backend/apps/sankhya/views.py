from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status

from clients.sankhya.auth import get_valid_token
from clients.sankhya.product import get_product


class ProductDetailView(APIView):
    """
    Busca detalhes de um produto no Sankhya pelo código.
    Rate limit: 60 requisições por minuto por usuário.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "sankhya"

    def get(self, request, code):
        """
        Retorna dados do produto.
        """
        if not code:
            return Response(
                {"detail": "Código do produto é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = get_valid_token()
        product_data = get_product(code, token)

        return Response(product_data)
