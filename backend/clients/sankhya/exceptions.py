"""Exceções do client Sankhya (auth e product)."""


class SankhyaAuthError(Exception):
    """Erro de autenticação ou renovação de token Sankhya."""

    pass


class SankhyaProductError(Exception):
    """Erro ao buscar produto na API Sankhya."""

    pass
