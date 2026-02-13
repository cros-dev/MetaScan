"""Cliente Sankhya: auth (login legado) e product (API V1)."""

from clients.sankhya.auth import get_valid_token, login as sankhya_login, refresh_token_if_needed
from clients.sankhya.exceptions import SankhyaAuthError, SankhyaProductError
from clients.sankhya.product import get_product

__all__ = [
    "SankhyaAuthError",
    "SankhyaProductError",
    "get_product",
    "get_valid_token",
    "refresh_token_if_needed",
    "sankhya_login",
]
