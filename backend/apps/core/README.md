# App: Core

Funcionalidades transversais e utilitários do sistema.

## Componentes

### Permissions (`permissions.py`)
Classes de permissão customizadas para DRF:
- `IsAdmin`: Apenas Admin.
- `IsManager`: Manager ou Admin.
- `IsAuditor`: Auditor, Manager ou Admin.
- `IsOwnerOrReadOnly`: Edição apenas para o dono do objeto.

### Utils (`utils.py`)
Funções auxiliares:
- Formatação de CPF/CNPJ.
- Formatação de telefone.

### Validators (`validators.py`)
Validadores de modelo/serializer:
- Validação de CPF e CNPJ.

### Messages (`messages.py`)
Central de mensagens de erro e sucesso para padronização da API.
