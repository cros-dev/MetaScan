"""
Testes automatizados para os serviços de autenticação e consulta de produto da Sankhya.
Utiliza pytest e unittest.mock para simular respostas da API externa.
"""

import pytest
from unittest.mock import patch
from core.services import sankhya_auth, sankhya_product

@patch("core.services.sankhya_auth.requests.post")
def test_sankhya_login_success(mock_post):
    """
    Testa login bem-sucedido na Sankhya (retorna token).
    """
    class User:
        id = 1
        email = "user@example.com"
        sankhya_password = "password"
    fake_user = User()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"bearerToken": "token123"}
    token = sankhya_auth.sankhya_login(fake_user.email, fake_user.sankhya_password)
    assert token == "token123"

@patch("core.services.sankhya_auth.requests.post")
def test_sankhya_login_fail(mock_post):
    """
    Testa login falho na Sankhya (retorna None).
    """
    class User:
        id = 1
        email = "user@example.com"
        sankhya_password = "password"
    fake_user = User()
    mock_post.return_value.status_code = 401
    mock_post.return_value.text = "Unauthorized"
    token = sankhya_auth.sankhya_login(fake_user.email, fake_user.sankhya_password)
    assert token is None

@patch("core.services.sankhya_product.get_valid_token")
@patch("core.services.sankhya_product.User")
@patch("core.services.sankhya_product.requests.post")
def test_consult_sankhya_product_success(mock_post, mock_user, mock_get_token):
    """
    Testa consulta de produto bem-sucedida na Sankhya.
    """
    fake_user = mock_user.objects.filter.return_value.first.return_value
    fake_user.id = 1
    fake_user.email = "user@example.com"
    fake_user.sankhya_password = "password"
    mock_get_token.return_value = "token123"
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "responseBody": {
            "produtos": {
                "produto": {
                    "CODPROD": {"$": "123"},
                    "DESCRPROD": {"$": "Produto Teste"},
                    "Cadastro_MARCA": {"$": "MAKITA"},
                    "Cadastro_REFFORN": {"$": "REF-123"},
                    "Cadastro_LOCALIZACAO": {"$": "CAV-01-A1"},
                    "Cadastro_AD_DTAINVENTARIO": {"$": "17/05/2025 00:00:00"},
                    "PRECOBASE": {"$": "100.00"},
                    "Estoque_1": {"$": "5.0000"},
                    "CODVOL": {"$": "PC"}
                }
            }
        }
    }
    result = sankhya_product.consult_sankhya_product("123", fake_user.id)
    expected = {
        "code": "123",
        "description": "Produto Teste",
        "marca": "MAKITA",
        "referencia_fornecedor": "REF-123",
        "localizacao": "CAV-01-A1",
        "data_inventario": "17/05/2025 00:00:00",
        "preco_base": "100.00",
        "estoque": "5.0000",
        "unidade": "PC"
    }
    assert result == expected

@patch("core.services.sankhya_product.get_valid_token")
@patch("core.services.sankhya_product.User")
@patch("core.services.sankhya_product.requests.post")
def test_consult_sankhya_product_not_found(mock_post, mock_user, mock_get_token):
    """
    Testa consulta de produto que não existe (retorna None).
    """
    fake_user = mock_user.objects.filter.return_value.first.return_value
    fake_user.id = 1
    fake_user.email = "user@example.com"
    fake_user.sankhya_password = "password"
    mock_get_token.return_value = "token123"
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "responseBody": {
            "produtos": {}
        }
    }
    result = sankhya_product.consult_sankhya_product("123", fake_user.id)
    assert result is None

@patch("core.services.sankhya_product.get_valid_token")
@patch("core.services.sankhya_product.User")
def test_consult_sankhya_product_auth_error(mock_user, mock_get_token):
    """
    Testa erro de autenticação ao consultar produto na Sankhya.
    """
    fake_user = mock_user.objects.filter.return_value.first.return_value
    fake_user.id = 1
    fake_user.email = "user@example.com"
    fake_user.sankhya_password = "password"
    mock_get_token.side_effect = sankhya_auth.SankhyaAuthError("Erro de autenticação")
    with pytest.raises(sankhya_auth.SankhyaAuthError):
        sankhya_product.consult_sankhya_product("123", fake_user.id) 