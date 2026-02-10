## O que é o MetaScan

O **MetaScan** é um sistema de **conferência de estoque em cavaletes** para apoio à auditoria e ao controle de inventário. Permite cadastrar cavaletes e posições (slots), atribuir responsáveis, registrar produtos e quantidades por slot e acompanhar o fluxo de conferência (disponível → em conferência → concluído). A aplicação integra-se ao **ERP Sankhya** para validar códigos de produto e consultar dados de estoque em tempo real.

---

## Objetivo

Oferecer uma API e interfaces (web e futuramente mobile) para que gestores e conferentes realizem a conferência de estoque nos cavaletes de forma rastreável, com histórico de ações e validação de produtos via Sankhya.

---

## Público-alvo

- **Conferentes:** usuários que realizam a conferência nos cavaletes atribuídos a eles (edição de produto/quantidade nos slots em conferência).
- **Gestores:** visualizam cavaletes e históricos, aprovam ou finalizam conferências, atribuem cavaletes a conferentes.
- **Administradores:** gestão completa de usuários, cavaletes, exportação de dados (ex.: Excel) e configuração.

---

## Escopo do MVP

- Autenticação por email com JWT e integração opcional com Sankhya (validação de credenciais).
- Cadastro de cavaletes com slots (lados A/B, posições numeradas); a quantidade de slots por cavalete é definida pelo usuário no frontend. Atribuição de cavaletes a usuários.
- Workflow de conferência em slots: disponível → em conferência → concluído; edição de produto/quantidade apenas quando o slot está em conferência.
- Consulta de produto no Sankhya por código (validação e dados de estoque/descrição).
- Histórico de ações em slots e cavaletes (auditoria).
- Gestão de usuários com papéis (admin, gestor, conferente) e desativação/reativação.

---

## Fora de escopo (por enquanto)

- Relatórios analíticos e dashboards avançados.
- App mobile completo (estrutura pode existir para uso futuro).
- MinIO/armazenamento de arquivos (pode ser adicionado depois se necessário).

---

**Status:** Visão do produto MetaScan  
**Última atualização:** 2026-02-09
