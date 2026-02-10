# Guia Postman - MetaScan Backend

Este documento descreve o padrão de organização e boas práticas para usar o **Postman** no desenvolvimento da API.

## Estrutura da Collection

A Collection deve seguir a hierarquia abaixo:

- **Project API** (Root)
  - **Auth** (Autenticação JWT)
    - `POST Login`
    - `POST Refresh Token`
  - **Users** (Perfil do usuário logado)
    - `GET My Profile`
    - `PATCH My Profile`
  - **Admin** (Gestão administrativa)
    - `GET User by ID`
    - `PATCH User by ID`
    - `DEL User by ID`

---

## Collection Variables

Use variáveis para tokens e URLs:

| Variável | Valor Exemplo | Descrição |
| :--- | :--- | :--- |
| `base_url` | `http://localhost:8000/api` | URL base da API |
| `django_access_token` | `eyJhbGci...` | Token JWT de acesso |
| `django_refresh_token` | `eyJhbGci...` | Token JWT de atualização |

## Automação de Token (Script)

Adicione o seguinte script na aba **Tests** da requisição `POST Login` para capturar os tokens automaticamente:

```javascript
const json = pm.response.json();

if (json.access) {
    pm.collectionVariables.set("django_access_token", json.access);
    console.log("Access token salvo");
}

if (json.refresh) {
    pm.collectionVariables.set("django_refresh_token", json.refresh);
    console.log("Refresh token salvo");
}
```

---

## Autenticação

Todas as requisições (exceto o Login) devem utilizar o tipo de autenticação **Bearer Token** na aba **Authorization**:

- **Type**: `Bearer Token`
- **Token**: `{{django_access_token}}`

> **Dica**: Configure a autenticação no nível da pasta raiz (ou subpastas) e use a opção "Inherit auth from parent" em cada request individual.

---

## Observações Gerais

- **Nomenclatura**: Use nomes descritivos em inglês para requests e pastas.
- **Exemplos**: Sempre que implementar um novo endpoint, salve um exemplo de "Success" e "Error" na Collection.
- **Headers**: Certifique-se de que o `Content-Type: application/json` está configurado para requests de envio de dados (POST/PATCH/PUT).
- **Sincronização**: Considere exportar o JSON da Collection para o repositório em `docs/postman/` para versionamento.

---

**Status:** Guia padronizado  
**Última atualização:** 2026-01-26
