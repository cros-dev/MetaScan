# Especificação de API - MetaScan

Este documento descreve os endpoints da API do MetaScan (conferência de estoque em cavaletes, integração Sankhya).

## Autenticação

- `POST /api/token/` - Login (access/refresh)
- `POST /api/token/refresh/` - Renovação do access token
- `POST /api/token/verify/` - Verificação de token

## Usuários

- `GET /api/users/profile/` - Perfil do usuário logado
- `PATCH /api/users/profile/` - Atualização do perfil logado
- `GET /api/users/{id}/` - Detalhes de usuário (admin)

---

**Status:** Especificação da API MetaScan (será ampliada com cavaletes, slots, históricos, Sankhya)  
**Última atualização:** 2026-02-09
