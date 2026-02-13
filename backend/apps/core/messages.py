from django.utils.translation import gettext_lazy as _

# =========================================================
# GENERIC MESSAGES
# =========================================================
PERMISSION_DENIED = _("Você não tem permissão para realizar esta ação.")
NOT_FOUND = _("Registro não encontrado.")
INVALID_INPUT = _("Dados inválidos.")
UNAUTHORIZED = _("Credenciais inválidas.")

# =========================================================
# AUTH MESSAGES
# =========================================================
USER_INACTIVE = _("Usuário inativo.")
USER_NOT_FOUND = _("Usuário não encontrado.")
PASSWORD_MISMATCH = _("Senha incorreta.")

# =========================================================
# VALIDATION MESSAGES
# =========================================================
REQUIRED_FIELD = _("Este campo é obrigatório.")
INVALID_CPF = _("CPF inválido.")
INVALID_CNPJ = _("CNPJ inválido.")
INVALID_DATE = _("Data inválida.")
