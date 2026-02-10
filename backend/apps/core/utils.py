"""
Utilitários genéricos para o app core.

Funções auxiliares reutilizáveis em todo o projeto.
"""


def format_phone(phone: str) -> str:
    """
    Formata número de telefone removendo caracteres não numéricos.

    Args:
        phone: Número de telefone com ou sem formatação

    Returns:
        String apenas com dígitos
    """
    return "".join(filter(str.isdigit, str(phone)))


def format_cpf(cpf: str) -> str:
    """
    Formata CPF no padrão XXX.XXX.XXX-XX.

    Args:
        cpf: CPF com ou sem formatação

    Returns:
        CPF formatado
    """
    cpf_clean = "".join(filter(str.isdigit, str(cpf)))
    if len(cpf_clean) == 11:
        return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
    return cpf_clean


def format_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX.

    Args:
        cnpj: CNPJ com ou sem formatação

    Returns:
        CNPJ formatado
    """
    cnpj_clean = "".join(filter(str.isdigit, str(cnpj)))
    if len(cnpj_clean) == 14:
        return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}"
    return cnpj_clean
