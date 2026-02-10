"""Testes dos validators do app core."""

from django.test import TestCase
from django.core.exceptions import ValidationError

from ..validators import validate_cpf, validate_cnpj


class ValidatorsTestCase(TestCase):
    """Testes para validators."""

    def test_validate_cpf_valid(self):
        """Testa validação de CPF válido."""
        try:
            validate_cpf("12345678909")
            validate_cpf("123.456.789-09")
        except ValidationError:
            self.fail("validate_cpf() levantou ValidationError para CPF válido")

    def test_validate_cpf_invalid_length(self):
        """Testa validação de CPF com tamanho inválido."""
        with self.assertRaises(ValidationError):
            validate_cpf("1234567890")  # 10 dígitos

    def test_validate_cpf_invalid_repeated(self):
        """Testa validação de CPF com dígitos repetidos."""
        with self.assertRaises(ValidationError):
            validate_cpf("11111111111")

    def test_validate_cpf_empty(self):
        """Testa validação de CPF vazio."""
        try:
            validate_cpf("")
            validate_cpf(None)
        except ValidationError:
            self.fail("validate_cpf() não deve validar valores vazios")

    def test_validate_cnpj_valid(self):
        """Testa validação de CNPJ válido."""
        try:
            validate_cnpj("12345678000190")
            validate_cnpj("12.345.678/0001-90")
        except ValidationError:
            self.fail("validate_cnpj() levantou ValidationError para CNPJ válido")

    def test_validate_cnpj_invalid_length(self):
        """Testa validação de CNPJ com tamanho inválido."""
        with self.assertRaises(ValidationError):
            validate_cnpj("1234567800019")  # 13 dígitos

    def test_validate_cnpj_invalid_repeated(self):
        """Testa validação de CNPJ com dígitos repetidos."""
        with self.assertRaises(ValidationError):
            validate_cnpj("11111111111111")
