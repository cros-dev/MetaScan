import requests
import json
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.sankhya_product import consult_sankhya_product, SankhyaAuthError

class ProductConsultView(APIView):
    """
    Endpoint para consultar produtos na Sankhya.
    Requer autenticação e retorna dados do produto consultado pelo código.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        user_id = request.user.id
        try:
            product = consult_sankhya_product(code, user_id)
        except SankhyaAuthError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except requests.RequestException:
            return Response({"detail": "Erro de conexão com a Sankhya."}, status=status.HTTP_502_BAD_GATEWAY)
        except json.JSONDecodeError:
            return Response({"detail": "Erro ao processar resposta da Sankhya (JSON inválido)."}, status=status.HTTP_502_BAD_GATEWAY)
        if product:
            return Response(product)
        return Response({"detail": "Produto não encontrado na Sankhya."}, status=status.HTTP_404_NOT_FOUND)
