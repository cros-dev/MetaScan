"""Utilitários genéricos do app core (formatação reutilizável)."""


def format_phone(phone: str) -> str:
    """Remove caracteres não numéricos e retorna string apenas com dígitos."""
    return "".join(filter(str.isdigit, str(phone)))


def format_cpf(cpf: str) -> str:
    """Formata CPF no padrão XXX.XXX.XXX-XX."""
    cpf_clean = "".join(filter(str.isdigit, str(cpf)))
    if len(cpf_clean) == 11:
        return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
    return cpf_clean


def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX."""
    cnpj_clean = "".join(filter(str.isdigit, str(cnpj)))
    if len(cnpj_clean) == 14:
        return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}"
    return cnpj_clean
