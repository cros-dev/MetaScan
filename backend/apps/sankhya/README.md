# App: Sankhya

Gateway de integração com o ERP Sankhya.

## Responsabilidade
Atuar como proxy para consultas à API do Sankhya, gerenciando autenticação e tratamento de erros.

## Funcionalidades

- **Autenticação:** Gerencia token de sessão do Sankhya (login/refresh) usando credenciais de serviço globais.
- **Cache:** Armazena token para evitar logins repetitivos.
- **Proxy:** Repassa dados do produto do ERP para o Frontend.

## Client
A lógica de comunicação fica isolada em `backend/clients/sankhya/`.

## Endpoints

- `GET /api/sankhya/products/<code_produto>/`: Retorna detalhes do produto (descrição, etc).
