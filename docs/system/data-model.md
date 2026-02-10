## Modelo de Dados - MetaScan

Este documento descreve o modelo de dados do MetaScan em alto nível.

### Usuário (CustomUser)

Login por email; papéis: admin, gestor, conferente. Senha Sankhya (criptografada) para integração com o ERP.

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| id | Int | Sim | Identificador |
| email | String | Sim | Login (único) |
| first_name, last_name | String | Não | Nome |
| role | String | Sim | admin / manager / auditor |
| is_active | Boolean | Sim | Status |
| sankhya_password | Encrypted | Não | Senha para API Sankhya |

### Cavalete

Estrutura física com código (ex.: CAV01), tipo (corredor/torre), usuário atribuído e status.

### Slot

Posição no cavalete (lado A/B + número). Produto, descrição, quantidade e status (available, auditing, completed).

### SlotHistory / CavaleteHistory

Registros de auditoria: quem fez qual ação e quando (slots e cavaletes).

---

**Status:** Modelo do MetaScan (será detalhado com cavaletes, slots, históricos)  
**Última atualização:** 2026-02-09
