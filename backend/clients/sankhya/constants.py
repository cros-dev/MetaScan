"""Paths e chaves fixas da API Sankhya (URL base, appkey e token vêm do .env)."""

# Login legado
LOGIN_PATH = "/login"
RESPONSE_BEARER_KEY = "bearerToken"
HEADER_TOKEN = "token"
HEADER_APPKEY = "appkey"
HEADER_USERNAME = "username"
HEADER_PASSWORD = "password"
BEARER_CACHE_TIMEOUT_SECONDS = 25 * 60

# HTTP
SANKHYA_HTTP_TIMEOUT = 30

# API V1
PRODUTOS_PATH = "/v1/produtos"
