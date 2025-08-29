import logging
import os
import requests
from django.contrib.auth import get_user_model
from sankhya.services.sankhya_auth import get_valid_token, SankhyaAuthError

"""
Serviço responsável por consultar produtos na API Sankhya.
"""

User = get_user_model()

SANKHYA_API_BASE_URL = os.environ['SANKHYA_API_BASE_URL']
SANKHYA_PRODUCT_PATH = os.environ['SANKHYA_PRODUTO_PATH']
SANKHYA_PRODUCT_URL = f'{SANKHYA_API_BASE_URL}{SANKHYA_PRODUCT_PATH}'

def consult_sankhya_product(product_code, user_id):
    """
    Consulta produto na Sankhya usando CRUDServiceProvider.loadRecords.
    Retorna dict com code e description, ou None se não encontrado.
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
        "serviceName": "CRUDServiceProvider.loadRecords",
        "requestBody": {
            "dataSet": {
                "rootEntity": "Estoque",
                "includePresentationFields": "S",
                "offsetPage": "0",
                "criteria": {
                    "expression": {"$": "this.CODPROD = ?"},
                    "parameter": [
                        {"$": str(product_code), "type": "I"}
                    ]
                },
                "entity": {
                    "fieldset": {
                        "list": "CODPROD,CODLOCAL,CODEMP,CONTROLE,ESTOQUE,RESERVADO,WMSBLOQUEADO,DTFABRICACAO,DTVAL,ATIVO,TIPO,CODPARC"
                    }
                }
            }
        }
    }
    logging.info(f'Consultando produto {product_code} na Sankhya (CRUDServiceProvider). URL: {url}')
    response = requests.post(url, headers=headers, json=body)
    logging.info(f'Resposta Sankhya para produto {product_code}: Status {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        logging.info(f'Dados Sankhya para produto {product_code}: {data}')
        try:
            estoque_list = (
                data.get('responseBody', {})
                    .get('entities', {})
                    .get('entity', [])
            )
            if not estoque_list:
                logging.warning(f'Produto {product_code} não encontrado no estoque: {data}')
                return None
            produto = estoque_list[0]
            code = produto.get('f0', {}).get('$')
            description = produto.get('f12', {}).get('$', '')
            return {"code": code, "description": description}
        except (KeyError, TypeError, ValueError) as e:
            logging.exception(f'Erro ao processar resposta Sankhya para produto {product_code}: {e}')
            return None
    elif response.status_code in [401, 403]:
        logging.error(f'Falha de autenticação Sankhya para user_id={user_id}. Token pode estar inválido.')
        raise SankhyaAuthError('Não foi possível autenticar na Sankhya.')
    else:
        logging.error(f'Erro na requisição Sankhya para produto {product_code}. Status: {response.status_code}, Response: {response.text}')
    return None
