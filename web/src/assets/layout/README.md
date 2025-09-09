# Guia de Estilização do Projeto

Este documento descreve a estrutura, organização e boas práticas para a estilização do frontend deste projeto Angular.

---

## Estrutura de Pastas

```
src/assets/layout/
  _core.scss           # Estilos globais, resets, containers principais
  _menu.scss           # Estilos do menu lateral (sidebar)
  _topbar.scss         # Estilos da topbar
  _responsive.scss     # Media queries e responsividade
  _utils.scss          # Mixins e utilitários (se necessário)
  layout.scss          # Arquivo principal que importa todos os outros
  variables/
    _common.scss       # Variáveis CSS comuns a todos os temas
    _light.scss        # Variáveis do tema claro
    _dark.scss         # Variáveis do tema escuro
```

---

## Organização dos Estilos

- **layout.scss**: ponto de entrada dos estilos globais do app. Usa `@use` para importar todos os arquivos SCSS do layout.
- **_core.scss**: define resets, estilos globais, containers principais e alinhamentos.
- **_menu.scss**: estilos da sidebar, menu, seções e itens ativos.
- **_topbar.scss**: estilos da barra superior (topbar).
- **_responsive.scss**: regras de responsividade para sidebar, menu e conteúdo.
- **variables/_common.scss**: centraliza variáveis CSS usadas em ambos os temas.
- **variables/_light.scss**: define variáveis para o tema claro (cores, fundo, texto, etc).
- **variables/_dark.scss**: define variáveis para o tema escuro.

---

## Temas (Claro/Escuro)

- O tema é alternado adicionando/removendo a classe `app-dark` no elemento `<html>`.
- As variáveis CSS são sobrescritas em `:root` (tema claro) e `:root[class*='app-dark']` (tema escuro).
- A preferência de tema é salva no `localStorage` e restaurada automaticamente.

---

## Variáveis CSS

- Todas as cores, espaçamentos e bordas usam variáveis CSS para facilitar manutenção e customização.
- Exemplos:
  - `--surface-ground`: fundo principal do app
  - `--surface-card`: fundo de cards/topbar
  - `--surface-overlay`: fundo da sidebar
  - `--text-color`: cor do texto principal
  - `--primary-color`: cor primária do tema (#3b82f6)
  - `--sidebar-width`: largura da sidebar (22rem)
  - `--topbar-height`: altura da topbar (6rem)
  - `--content-padding`: padding do conteúdo (1.5rem)

---

## Boas Práticas

- Sempre use variáveis CSS para cores e espaçamentos.
- Mantenha os estilos de cada componente em arquivos separados.
- Use `@use` no lugar de `@import` para importar arquivos SCSS.
- Centralize regras de responsividade em `_responsive.scss`.
- Evite sobrescrever estilos globais; prefira classes específicas do layout.
- Para novos temas, crie um novo arquivo em `variables/` e siga o padrão.

---

## Como adicionar um novo tema

1. Crie um arquivo em `src/assets/layout/variables/` (ex: `_blue.scss`).
2. Defina as variáveis CSS desejadas em `:root` ou `:root[class*='app-blue']`.
3. Importe o novo arquivo em `layout.scss` usando `@use`.
4. Adapte a lógica de alternância de tema no serviço/layout.

---

## Observações

- Os estilos foram modularizados para facilitar manutenção e escalabilidade.
- Qualquer ajuste futuro nos temas deve ser feito nos arquivos de variáveis.
- Para dúvidas ou sugestões, consulte este README antes de alterar estilos globais. 