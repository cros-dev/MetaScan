"""
Validators genéricos para o app core.

Validators reutilizáveis que podem ser usados em qualquer app do projeto.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cpf(value):
    """
    Validador robusto de CPF com algoritmo de dígitos verificadores.
    """
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
    """
    Validador básico de CNPJ.

    Remove formatação e valida se tem 14 dígitos numéricos.
    Para validação completa, considere usar biblioteca externa.
    """
    if not value:
        return

    cnpj = "".join(filter(str.isdigit, str(value)))

    if len(cnpj) != 14:
        raise ValidationError(_("CNPJ deve conter 14 dígitos."))

    if cnpj == cnpj[0] * 14:
        raise ValidationError(_("CNPJ inválido."))
