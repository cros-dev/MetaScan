"""Login legado Sankhya (POST /login) e cache do bearerToken para chamadas subsequentes."""

import logging

import requests
from django.conf import settings
from django.core.cache import cache

from clients.sankhya.constants import (
    BEARER_CACHE_TIMEOUT_SECONDS,
    HEADER_APPKEY,
    HEADER_PASSWORD,
    HEADER_TOKEN,
    HEADER_USERNAME,
    LOGIN_PATH,
    RESPONSE_BEARER_KEY,
    SANKHYA_HTTP_TIMEOUT,
)
from clients.sankhya.exceptions import SankhyaAuthError

logger = logging.getLogger(__name__)


def _login_url():
    base = (getattr(settings, "SANKHYA_API_BASE_URL", None) or "").rstrip("/")
    return f"{base}{LOGIN_PATH}"


def _build_login_headers(appkey: str, token: str, username: str, password: str) -> dict:
    """Monta headers do POST /login (legado)."""
    return {
        HEADER_TOKEN: token,
        HEADER_APPKEY: appkey,
        HEADER_USERNAME: username,
        HEADER_PASSWORD: password,
    }


def login(username: str, password: str) -> str:
    """Login na API Sankhya (legado). Retorna bearerToken. Raises SankhyaAuthError em falha."""
    url = _login_url()
    appkey = getattr(settings, "SANKHYA_APPKEY", None)
    token = getattr(settings, "SANKHYA_TOKEN", None)
    if not url or url == LOGIN_PATH or not appkey or not token:
        logger.error("SANKHYA_API_BASE_URL, SANKHYA_APPKEY e SANKHYA_TOKEN devem estar configurados.")
        raise SankhyaAuthError("SANKHYA_API_BASE_URL, SANKHYA_APPKEY e SANKHYA_TOKEN devem estar configurados.")

    headers = _build_login_headers(appkey, token, username, password)
    try:
        response = requests.post(url, headers=headers, timeout=SANKHYA_HTTP_TIMEOUT)
    except requests.RequestException as e:
        logger.exception("Erro de rede ao chamar Sankhya /login: %s", e)
        raise SankhyaAuthError("Erro de rede ao chamar Sankhya /login.") from e
    if response.status_code != 200:
        logger.warning("Sankhya /login retornou status %s para user=%s", response.status_code, username)
        raise SankhyaAuthError(f"Login Sankhya falhou (status {response.status_code}).")
    try:
        data = response.json()
    except ValueError:
        logger.error("Resposta não-JSON do /login Sankhya: %s", response.text[:500])
        raise SankhyaAuthError("Resposta inválida do /login Sankhya (não-JSON).")
    if not isinstance(data, dict):
        raise SankhyaAuthError("Resposta inválida do /login Sankhya.")
    bearer = data.get(RESPONSE_BEARER_KEY)
    if not bearer:
        logger.warning("BearerToken ausente na resposta Sankhya. error=%s", data.get("error"))
        raise SankhyaAuthError("BearerToken ausente na resposta Sankhya.")
    return bearer


def get_valid_token(user, force_refresh: bool = False) -> str:
    """BearerToken válido para o user (cache + renovação). Raises SankhyaAuthError se falhar."""
    if not user or not getattr(user, "sankhya_password", None):
        uid = getattr(user, "id", None)
        logger.error("Usuário não encontrado ou senha Sankhya ausente para user_id=%s.", uid)
        raise SankhyaAuthError("Não foi possível autenticar na Sankhya (usuário ou senha ausente).")

    cache_key = f"sankhya:v1:token:{user.id}"
    cached = cache.get(cache_key)

    if force_refresh or not cached:
        logger.info("Token Sankhya não em cache ou refresh forçado para user_id=%s. Renovando login.", user.id)
        try:
            cached = login(user.email, user.sankhya_password)
            cache.set(cache_key, cached, timeout=BEARER_CACHE_TIMEOUT_SECONDS)
        except SankhyaAuthError as e:
            logger.error("Falha ao renovar token Sankhya para user_id=%s.", user.id)
            raise SankhyaAuthError("Não foi possível autenticar na Sankhya (login de renovação falhou).") from e

    return cached


def refresh_token_if_needed(user, response_status_code: int) -> bool:
    """Limpa cache do token se response_status_code for 401 ou 403. Retorna True se limpou."""
    if response_status_code in (401, 403):
        cache_key = f"sankhya:v1:token:{user.id}"
        cache.delete(cache_key)
        logger.warning("Token Sankhya invalidado (status %s) para user_id=%s. Cache limpo.", response_status_code, user.id)
        return True
    return False
