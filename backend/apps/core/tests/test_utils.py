"""
Testes para funções utilitárias do app core.
"""

from django.test import TestCase

from ..utils import format_phone, format_cpf, format_cnpj


class UtilsTestCase(TestCase):
    """Testes para funções utilitárias."""

    def test_format_phone(self):
        """Testa formatação de telefone."""
        self.assertEqual(format_phone("(11) 98765-4321"), "11987654321")
        self.assertEqual(format_phone("11 98765 4321"), "11987654321")
        self.assertEqual(format_phone("11987654321"), "11987654321")

    def test_format_cpf(self):
        """Testa formatação de CPF."""
        self.assertEqual(format_cpf("12345678901"), "123.456.789-01")
        self.assertEqual(format_cpf("123.456.789-01"), "123.456.789-01")
        self.assertEqual(
            format_cpf("123"), "123"
        )  # CPF inválido retorna sem formatação

    def test_format_cnpj(self):
        """Testa formatação de CNPJ."""
        self.assertEqual(format_cnpj("12345678000190"), "12.345.678/0001-90")
        self.assertEqual(format_cnpj("12.345.678/0001-90"), "12.345.678/0001-90")
        self.assertEqual(
            format_cnpj("123"), "123"
        )  # CNPJ inválido retorna sem formatação
