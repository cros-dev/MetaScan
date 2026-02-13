"""Cliente Sankhya V1: GET /v1/produtos/{codigoProduto}. Requer bearerToken em Authorization."""

import logging

import requests
from django.conf import settings

from clients.sankhya.constants import PRODUTOS_PATH, SANKHYA_HTTP_TIMEOUT
from clients.sankhya.exceptions import SankhyaProductError

logger = logging.getLogger(__name__)


def _base_url():
    return (getattr(settings, "SANKHYA_API_BASE_URL", None) or "").rstrip("/")


def _build_product_headers(bearer_token: str) -> dict:
    """Monta headers do GET /v1/produtos/{codigoProduto}."""
    return {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
    }


def get_product(codigo_produto: int, bearer_token: str) -> dict:
    """Busca produto por código na API V1. Retorna dict da API. Raises SankhyaProductError em falha."""
    base = _base_url()
    if not base:
        logger.error("SANKHYA_API_BASE_URL não configurado.")
        raise SankhyaProductError("SANKHYA_API_BASE_URL não configurado.")

    url = f"{base}{PRODUTOS_PATH}/{codigo_produto}"
    headers = _build_product_headers(bearer_token)
    try:
        response = requests.get(url, headers=headers, timeout=SANKHYA_HTTP_TIMEOUT)
    except requests.RequestException as e:
        logger.exception("Erro de rede ao buscar produto %s: %s", codigo_produto, e)
        raise SankhyaProductError("Erro de rede ao buscar produto.") from e

    if response.status_code == 404:
        logger.debug("Produto %s não encontrado.", codigo_produto)
        raise SankhyaProductError("Produto não encontrado.")
    if response.status_code != 200:
        logger.warning(
            "Sankhya produtos retornou status %s para codigo=%s", response.status_code, codigo_produto
        )
        raise SankhyaProductError(f"Sankhya produtos retornou status {response.status_code}.")

    try:
        data = response.json()
    except ValueError:
        logger.error(
            "Resposta não-JSON do Sankhya produtos %s: %s", codigo_produto, response.text[:500]
        )
        raise SankhyaProductError("Resposta inválida do Sankhya produtos (não-JSON).")
    if not isinstance(data, dict):
        raise SankhyaProductError("Resposta inválida do Sankhya produtos.")
    return data
