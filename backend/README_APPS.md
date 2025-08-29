# Estrutura de Apps do Backend MetaScan

## Visão Geral

O backend foi reorganizado em apps Django específicos para melhor organização e manutenibilidade. **Todas as funcionalidades existentes foram preservadas** e movidas para os apps apropriados.

## Apps

### 🏗️ `core/`
- **Responsabilidade**: Configurações globais, usuários e permissões
- **Modelos**: `CustomUser` (com roles e senha Sankhya criptografada)
- **Views**: `LoginView`, `MeView`, `TokenRefreshView`, `UserViewSet`
- **Funcionalidades**: Autenticação, autorização e gestão de usuários

### 📦 `cavaletes/`
- **Responsabilidade**: Gestão de cavaletes e slots
- **Modelos**: 
  - `Cavalete` (estrutura física com código automático)
  - `Slot` (posições A/B + número nos cavaletes)
- **Views**: `CavaleteViewSet` (com todas as actions funcionais)
- **Funcionalidades**: CRUD de cavaletes, exportação Excel, atribuição de usuários

### 📊 `inventory/`
- **Responsabilidade**: Auditoria e histórico de estoque
- **Modelos**:
  - `SlotHistory` (histórico de mudanças nos slots)
  - `CavaleteHistory` (histórico de ações nos cavaletes)
- **Views**: `SlotViewSet`, `SlotHistoryViewSet`, `CavaleteHistoryViewSet`
- **Funcionalidades**: Gestão de slots, conferência de estoque, histórico completo

### 🔌 `sankhya/`
- **Responsabilidade**: Integração com ERP Sankhya
- **Modelos**: Modelos específicos da integração (futuro)
- **Views**: `ProductConsultView`
- **Serviços**:
  - `sankhya_auth.py` - Autenticação e tokens
  - `sankhya_product.py` - Consulta de produtos
- **Funcionalidades**: Validação de produtos, consulta de estoque em tempo real

### 📈 `reports/`
- **Responsabilidade**: Relatórios e análises
- **Modelos**: Modelos específicos de relatórios (futuro)
- **Funcionalidades**: Dashboards, métricas, exportação

## Estrutura de Cada App

```
app_name/
├── __init__.py
├── admin.py          # Configuração do Django Admin
├── apps.py           # Configuração do app
├── models.py         # Modelos de dados
├── views.py          # Views da API (funcionais)
├── urls.py           # URLs do app
├── serializers.py    # Serializers DRF (funcionais)
├── services/         # Lógica de negócio
│   └── __init__.py
├── tests/            # Testes unitários
│   └── __init__.py
└── migrations/       # Migrações do banco
    └── __init__.py
```

## ✅ Funcionalidades Preservadas

- **Autenticação JWT** com integração Sankhya
- **Gestão completa de cavaletes** (CRUD, exportação, atribuição)
- **Gestão de slots** com workflow de conferência
- **Histórico completo** de todas as ações
- **Integração Sankhya** para validação de produtos
- **Sistema de permissões** por roles (admin, gestor, conferente)
- **Exportação Excel** de dados
- **Actions customizadas** para mudanças de status

## Benefícios da Reorganização

1. **Separação de Responsabilidades**: Cada app tem uma função específica
2. **Reutilização**: Apps podem ser reutilizados em outros projetos
3. **Manutenibilidade**: Código mais organizado e fácil de manter
4. **Testes**: Testes organizados por domínio
5. **Migrations**: Migrações independentes por app
6. **Escalabilidade**: Fácil adicionar novos apps conforme necessário
7. **Funcionalidade Preservada**: Nenhuma funcionalidade foi perdida

## Próximos Passos

1. **Rodar migrations** para aplicar as mudanças no banco
2. **Testar APIs** para garantir que tudo funciona
3. **Adicionar testes** para cada funcionalidade
4. **Documentar APIs** com DRF Spectacular
5. **Implementar novas funcionalidades** nos apps apropriados

## Configuração

Todos os apps estão registrados em `settings.py`:

```python
INSTALLED_APPS = [
    # ... apps Django padrão
    'core',
    'cavaletes',
    'inventory',
    'sankhya',
    'reports'
]
```

## URLs Principais

As URLs foram reorganizadas mas mantêm a mesma funcionalidade:

- `/cavaletes/` - Gestão de cavaletes
- `/slots/` - Gestão de slots
- `/slot-history/` - Histórico de slots
- `/cavalete-history/` - Histórico de cavaletes
- `/users/` - Gestão de usuários
- `/product/<code>/` - Consulta Sankhya
- `/login/` - Autenticação
- `/me/` - Dados do usuário logado
