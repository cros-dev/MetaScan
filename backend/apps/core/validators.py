"""Validators genéricos do app core (reutilizáveis no projeto)."""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cpf(value):
    """Valida CPF (11 dígitos e dígitos verificadores)."""
    if not value:
        return

    cpf = "".join(filter(str.isdigit, str(value)))

    if len(cpf) != 11:
        raise ValidationError(_("CPF deve conter 11 dígitos."))

    if cpf == cpf[0] * 11:
        raise ValidationError(_("CPF inválido."))

    for i in range(9, 11):
        value_sum = sum((int(cpf[num]) * ((i + 1) - num) for num in range(i)))
        digit = ((value_sum * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValidationError(_("CPF inválido."))


def validate_cnpj(value):
    """Valida CNPJ (14 dígitos). Validação básica; para completa use lib externa."""
    if not value:
        return

    cnpj = "".join(filter(str.isdigit, str(value)))

    if len(cnpj) != 14:
        raise ValidationError(_("CNPJ deve conter 14 dígitos."))

    if cnpj == cnpj[0] * 14:
        raise ValidationError(_("CNPJ inválido."))
