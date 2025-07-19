# MetaScan Web

Base para projetos Angular modernos, com PrimeNG, estrutura escalável e boas práticas.

## 📁 Estrutura de Pastas

```text
src/
  app/
    core/
      guards/
      interceptors/
      services/
      models/
    shared/
      components/
        button/
        card/
      directives/
      pipes/
    layout/
      header/
      footer/
      sidebar/
    features/
      dashboard/
      user/
      product/
    pages/
      home/
      login/
      not-found/
  assets/
  environments/
  styles/
    themes/
```

- **core/**: Serviços, guards, interceptors e models globais.
- **shared/**: Componentes, pipes e diretivas reutilizáveis.
- **layout/**: Componentes de layout (header, footer, sidebar).
- **features/**: Funcionalidades isoladas, ideais para lazy loading.
- **pages/**: Páginas principais (home, login, not-found).
- **assets/**: Imagens, fontes, etc.
- **environments/**: Configurações de ambiente.
- **styles/themes/**: Temas e estilos globais.

## 🚀 Primeiros Passos

1. **Instale as dependências:**
   ```bash
   npm install
   ```

2. **Rode o projeto:**
   ```bash
   ng serve
   ```
   Acesse em [http://localhost:4200](http://localhost:4200)

---
