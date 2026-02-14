## Modelo de Dados - MetaScan

Este documento descreve o modelo de dados do MetaScan em alto nível.

### Usuário (CustomUser)

Login por username (matrícula); papéis: admin, gestor, conferente.

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| id | Int | Sim | Identificador |
| username | String | Sim | Login (único) |
| email | String | Não | Email opcional |
| first_name, last_name | String | Não | Nome |
| role | Enum | Sim | ADMIN, MANAGER, AUDITOR |
| is_active | Boolean | Sim | Status |

### Cavalete

Estrutura física que contém slots.

| Campo | Tipo | Descrição |
| --- | --- | --- |
| id | Int | PK |
| code | String | Código único (ex: CAV-001) |
| type | Enum | DEFAULT (Padrão), PINE (Pinhal) |
| user | FK(User) | Conferente responsável |
| status | Enum | AVAILABLE, IN_PROGRESS, COMPLETED, BLOCKED |

### Slot

Posição no cavalete.

| Campo | Tipo | Descrição |
| --- | --- | --- |
| id | Int | PK |
| cavalete | FK(Cavalete) | Cavalete pai |
| side | Enum | A, B |
| number | Int | Número da posição |
| product_code | String | Código do produto conferido |
| quantity | Int | Quantidade conferida |
| status | Enum | AVAILABLE, AUDITING, COMPLETED |

### Histórico (CavaleteHistory / SlotHistory)

Logs de auditoria imutáveis.

| Campo | Tipo | Descrição |
| --- | --- | --- |
| ... | FK | Link para Cavalete ou Slot |
| user | FK(User) | Quem realizou a ação |
| action | Enum | CREATE, UPDATE, DELETE, ASSIGN, START_AUDIT, FINISH_AUDIT, etc. |
| timestamp | DateTime | Quando ocorreu |
| description | Text | Detalhes adicionais |
| snapshot | Fields | (Apenas SlotHistory) Dados antigos e novos |
