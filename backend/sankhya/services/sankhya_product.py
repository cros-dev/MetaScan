import json
import logging
import os
import requests
import time
from django.contrib.auth import get_user_model
from sankhya.services.sankhya_auth import get_valid_token, refresh_token_if_needed, SankhyaAuthError

"""
Serviço responsável por consultar produtos na API Sankhya.
"""

User = get_user_model()

SANKHYA_API_BASE_URL = os.environ['SANKHYA_API_BASE_URL']
SANKHYA_PRODUCT_PATH = os.environ['SANKHYA_PRODUTO_PATH']
SANKHYA_PRODUCT_URL = f'{SANKHYA_API_BASE_URL}{SANKHYA_PRODUCT_PATH}'

def consult_sankhya_product(product_code, user_id, max_retries=2):
    """
    Consulta produto na Sankhya usando ConsultaProdutosSP.consultaProdutos.
    Retorna dict com informações completas do produto, incluindo preço, estoque, marca, etc.
    
    Args:
        product_code: Código do produto a ser consultado
        user_id: ID do usuário para autenticação
        max_retries: Número máximo de tentativas em caso de erro de conexão
    """
    user = User.objects.filter(id=user_id).first()
    
    for attempt in range(max_retries + 1):
        try:
            # Na primeira tentativa, usa token do cache
            # Nas tentativas seguintes, força renovação se houve erro 401/403
            force_refresh = attempt > 0
            bearer_token = get_valid_token(user, force_refresh=force_refresh)
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
                        "CODPROD": {
                            "$": str(product_code)
                        }
                    },
                    "isPromocao": {
                        "$": "false"
                    },
                    "isLiquidacao": {
                        "$": "false"
                    }
                },
                "offsetPage": 0,
                "maxPageSize": 1
            }
        }
        
        logging.info(f'Consultando produto {product_code} na Sankhya (tentativa {attempt + 1}/{max_retries + 1})')
        
        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)
            logging.info(f'Resposta Sankhya para produto {product_code}: Status {response.status_code}')
            
            if response.status_code == 200:
                # Verificar se a resposta tem conteúdo antes de tentar fazer parse JSON
                if not response.text.strip():
                    logging.error(f'Resposta vazia da Sankhya para produto {product_code}')
                    return None
                
                try:
                    data = response.json()
                    logging.info(f'Dados Sankhya para produto {product_code}: {data}')
                except json.JSONDecodeError as e:
                    logging.error(f'Erro ao fazer parse JSON da resposta Sankhya para produto {product_code}: {e}. Response: {response.text}')
                    return None
                try:
                    produtos = data.get('responseBody', {}).get('produtos', {})
                    if not produtos:
                        logging.warning(f'Produto {product_code} não encontrado: {data}')
                        return None
                    
                    produto = produtos.get('produto', {})
                    if not produto:
                        logging.warning(f'Produto {product_code} não encontrado nos produtos: {data}')
                        return None
                    
                    # Extrair campos principais
                    code = produto.get('CODPROD', {}).get('$')
                    description = produto.get('DESCRPROD', {}).get('$', '').strip()
                    
                    # Extrair campos adicionais
                    marca = produto.get('Cadastro_MARCA', {}).get('$', '').strip()
                    referencia_fornecedor = produto.get('Cadastro_REFFORN', {}).get('$', '').strip()
                    localizacao = produto.get('Cadastro_LOCALIZACAO', {}).get('$', '').strip()
                    data_inventario = produto.get('Cadastro_AD_DTAINVENTARIO', {}).get('$', '')
                    
                    # Extrair informações de preço e estoque
                    preco_base = produto.get('PRECOBASE', {}).get('$', '0')
                    estoque = produto.get('Estoque_1', {}).get('$', '0')
                    unidade = produto.get('CODVOL', {}).get('$', '')
                    
                    return {
                        "code": code,
                        "description": description,
                        "marca": marca,
                        "referencia_fornecedor": referencia_fornecedor,
                        "localizacao": localizacao,
                        "data_inventario": data_inventario,
                        "preco_base": preco_base,
                        "estoque": estoque,
                        "unidade": unidade
                    }
                except (KeyError, TypeError, ValueError) as e:
                    logging.exception(f'Erro ao processar resposta Sankhya para produto {product_code}: {e}')
                    return None
                    
            elif response.status_code in [401, 403]:
                # Erro de autenticação - limpar cache e tentar novamente
                refresh_token_if_needed(user, response.status_code)
                if attempt < max_retries:
                    wait_time = (attempt + 1) * 2
                    logging.warning(f'Token Sankhya expirado (tentativa {attempt + 1}). Tentando renovar em {wait_time}s...')
                    time.sleep(wait_time)
                    continue
                else:
                    logging.error(f'Falha persistente de autenticação Sankhya após {max_retries + 1} tentativas')
                    raise SankhyaAuthError('Não foi possível autenticar na Sankhya.')
                
            elif response.status_code in [502, 503, 504]:
                # Erros de gateway/timeout - tentar novamente
                if attempt < max_retries:
                    wait_time = (attempt + 1) * 2  # 2s, 4s, 6s...
                    logging.warning(f'Erro de gateway/timeout na Sankhya (tentativa {attempt + 1}). Tentando novamente em {wait_time}s...')
                    time.sleep(wait_time)
                    continue
                else:
                    logging.error(f'Erro persistente de gateway/timeout na Sankhya após {max_retries + 1} tentativas')
                    raise requests.RequestException(f'Erro de conexão com a Sankhya (Status: {response.status_code})')
                    
            else:
                logging.error(f'Erro na requisição Sankhya para produto {product_code}. Status: {response.status_code}, Response: {response.text}')
                return None
                
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                wait_time = (attempt + 1) * 2
                logging.warning(f'Timeout na Sankhya (tentativa {attempt + 1}). Tentando novamente em {wait_time}s...')
                time.sleep(wait_time)
                continue
            else:
                logging.error(f'Timeout persistente na Sankhya após {max_retries + 1} tentativas')
                raise requests.RequestException('Timeout na conexão com a Sankhya')
                
        except requests.exceptions.ConnectionError:
            if attempt < max_retries:
                wait_time = (attempt + 1) * 2
                logging.warning(f'Erro de conexão com Sankhya (tentativa {attempt + 1}). Tentando novamente em {wait_time}s...')
                time.sleep(wait_time)
                continue
            else:
                logging.error(f'Erro de conexão persistente com Sankhya após {max_retries + 1} tentativas')
                raise requests.RequestException('Erro de conexão com a Sankhya')
                
        except requests.RequestException as e:
            logging.error(f'Erro na requisição Sankhya para produto {product_code}: {e}')
            raise
    
    return None
