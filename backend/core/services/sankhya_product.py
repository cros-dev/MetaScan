import logging
import os
import requests
from django.contrib.auth import get_user_model
from core.services.sankhya_auth import get_valid_token, SankhyaAuthError

"""
Serviço responsável por consultar produtos na API Sankhya.
"""

User = get_user_model()

SANKHYA_API_BASE_URL = os.environ['SANKHYA_API_BASE_URL']
SANKHYA_PRODUCT_PATH = os.environ['SANKHYA_PRODUTO_PATH']
SANKHYA_PRODUCT_URL = f'{SANKHYA_API_BASE_URL}{SANKHYA_PRODUCT_PATH}'

def consult_sankhya_product(product_code, user_id):
    """
    Checks if the product exists in Sankhya and returns a dict with code and description, or None.
    """
    user = User.objects.filter(id=user_id).first()
    try:
        bearer_token = get_valid_token(user)
    except SankhyaAuthError as e:
        logging.error(f'Erro de autenticação Sankhya: {e}')
        raise
    url = SANKHYA_PRODUCT_URL
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }
    body = {
        "serviceName": "ConsultaProdutosSP.consultaProdutos",
        "requestBody": {
            "filtros": {
                "criterio": {
                    "resourceID": "br.com.sankhya.com.cons.consultaProdutos",
                    "PERCDESC": "0",
                    "CODPROD": {"$": str(product_code)}
                },
                "isPromocao": {"$": "false"},
                "isLiquidacao": {"$": "false"}
            }
        }
    }
    logging.info(f'Consultando produto {product_code} na Sankhya. URL: {url}')
    response = requests.post(url, headers=headers, json=body)
    logging.info(f'Resposta Sankhya para produto {product_code}: Status {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        logging.info(f'Dados Sankhya para produto {product_code}: {data}')
        try:
            product = data["responseBody"]["produtos"]["produto"]
            code = product["CODPROD"]["$"]
            description = product.get("Cadastro_DESCRPROD", {}).get("$", "")
            if str(code) == str(product_code):
                logging.info(f'Produto {product_code} encontrado: {code} - {description}')
                return {"code": code, "description": description}
            logging.warning(f'Código produto não confere. Esperado: {product_code}, Recebido: {code}')
            return None
        except (KeyError, TypeError, ValueError):
            logging.exception(f'Erro ao processar resposta Sankhya para produto {product_code}')
            return None
    elif response.status_code in [401, 403]:
        logging.error(f'Falha de autenticação Sankhya para user_id={user_id}. Token pode estar inválido.')
        raise SankhyaAuthError('Não foi possível autenticar na Sankhya.')
    else:
        logging.error(f'Erro na requisição Sankhya para produto {product_code}. Status: {response.status_code}, Response: {response.text}')
    return None 