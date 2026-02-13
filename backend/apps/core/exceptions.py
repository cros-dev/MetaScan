"""Handler de exceções DRF: converte exceções de domínio em respostas HTTP."""

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from clients.sankhya.exceptions import SankhyaAuthError, SankhyaProductError


def custom_exception_handler(exc, context):
    """Chama o handler padrão do DRF; trata SankhyaAuthError e SankhyaProductError."""
    response = drf_exception_handler(exc, context)
    if response is not None:
        return response
    if isinstance(exc, SankhyaAuthError):
        return Response({"detail": str(exc)}, status=503)
    if isinstance(exc, SankhyaProductError):
        status = 404 if "Produto não encontrado" in str(exc) else 502
        return Response({"detail": str(exc)}, status=status)
    return None
