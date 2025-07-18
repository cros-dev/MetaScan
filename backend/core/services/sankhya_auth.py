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

def get_valid_token(user):
    """
    Retorna um token válido da Sankhya para o usuário, renovando e cacheando se necessário.
    """
    if not user or not user.sankhya_password:
        logging.error(f'Usuário não encontrado ou senha não salva para user_id={getattr(user, "id", None)}.')
        raise SankhyaAuthError('Não foi possível autenticar na Sankhya (usuário ou senha ausente).')
    cache_key = f'sankhya_token_{user.id}'
    bearer_token = cache.get(cache_key)
    if not bearer_token:
        logging.warning(f'Token Sankhya não encontrado no cache para user_id={user.id}. Tentando renovar login.')
        bearer_token = sankhya_login(user.email, user.sankhya_password)
        if bearer_token:
            logging.info(f'Novo token Sankhya obtido para user_id={user.id}.')
            cache.set(cache_key, bearer_token, timeout=60*60)
        else:
            logging.error(f'Falha ao renovar token Sankhya para user_id={user.id}.')
            raise SankhyaAuthError('Não foi possível autenticar na Sankhya (login de renovação falhou).')
    return bearer_token