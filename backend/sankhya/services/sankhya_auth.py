import logging
import os
import requests
from django.core.cache import cache

"""
Serviço responsável por autenticação (login, renovação e cache de token) com a API Sankhya.
"""

def sankhya_login(email, password):
    """
    Realiza login na API Sankhya e retorna o bearer token.
    """
    SANKHYA_API_BASE_URL = os.environ['SANKHYA_API_BASE_URL']
    SANKHYA_LOGIN_PATH = os.environ['SANKHYA_LOGIN_PATH']
    SANKHYA_LOGIN_URL = f'{SANKHYA_API_BASE_URL}{SANKHYA_LOGIN_PATH}'
    headers = {
        'AppKey': os.environ.get('SANKHYA_APPKEY'),
        'Token': os.environ.get('SANKHYA_TOKEN'),
        'username': email,
        'password': password,
    }
    response = requests.post(SANKHYA_LOGIN_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('bearerToken')
    return None

class SankhyaAuthError(Exception):
    pass

def get_valid_token(user, force_refresh=False):
    """
    Retorna um token válido da Sankhya para o usuário, renovando e cacheando se necessário.
    
    Args:
        user: Usuário Django
        force_refresh: Se True, força renovação mesmo se token existe no cache
    """
    if not user or not user.sankhya_password:
        logging.error(f'Usuário não encontrado ou senha não salva para user_id={getattr(user, "id", None)}.')
        raise SankhyaAuthError('Não foi possível autenticar na Sankhya (usuário ou senha ausente).')
    
    cache_key = f'sankhya_token_{user.id}'
    
    # Se forçar refresh ou não há token no cache, renovar
    if force_refresh or not cache.get(cache_key):
        logging.warning(f'Token Sankhya não encontrado no cache ou refresh forçado para user_id={user.id}. Tentando renovar login.')
        bearer_token = sankhya_login(user.email, user.sankhya_password)
        if bearer_token:
            logging.info(f'Novo token Sankhya obtido para user_id={user.id}.')
            # Cache por 50 minutos (menos que 1 hora para evitar expiração)
            cache.set(cache_key, bearer_token, timeout=50*60)
            return bearer_token
        else:
            logging.error(f'Falha ao renovar token Sankhya para user_id={user.id}.')
            raise SankhyaAuthError('Não foi possível autenticar na Sankhya (login de renovação falhou).')
    
    return cache.get(cache_key)

def refresh_token_if_needed(user, response_status_code):
    """
    Verifica se o token precisa ser renovado baseado no status da resposta.
    Se necessário, limpa o cache e força renovação.
    
    Args:
        user: Usuário Django
        response_status_code: Status code da resposta da API Sankhya
    """
    if response_status_code in [401, 403]:
        cache_key = f'sankhya_token_{user.id}'
        cache.delete(cache_key)
        logging.warning(f'Token Sankhya expirado para user_id={user.id}. Cache limpo.')
        return True
    return False
