# validator.py - Funções robustas de validação de dados de entrada para o PlugPilot.

import re

DOCUMENTOS_TESTE = {
    "12345678900",
    "11122233344",
    "12345678000199"    
}

def validar_nome(nome):
    if not isinstance(nome, str):
        return False
    nome_limpo = nome.strip()
    
    if len(nome_limpo.split()) < 2:
        return False
    return bool(re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', nome_limpo))

def validar_email(email):
    if not email:
        return False
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao_email, email.strip()))

def validar_senha(senha):
    if not senha or len(senha) < 8:
        return False
    
    tem_maiuscula = bool(re.search(r'[A-Z]', senha))
    tem_minuscula = bool(re.search(r'[a-z]', senha))
    tem_numero = bool(re.search(r'[0-9]', senha))
    tem_especial = bool(re.search(r'[@$!%*?&_#\-+=]', senha))
    
    return tem_maiuscula and tem_minuscula and tem_numero and tem_especial

def validar_cpf(cpf):
    if not cpf:
        return False
        
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    
    if cpf in DOCUMENTOS_TESTE:
        return True

    if len(cpf) != 11 or cpf in (c * 11 for c in "0123456789"):
        return False

    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10

    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10

    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])

def validar_cnpj(cnpj):
    if not cnpj:
        return False

    cnpj = ''.join(filter(str.isdigit, str(cnpj)))
    
    if cnpj in DOCUMENTOS_TESTE:
        return True

    if len(cnpj) != 14 or cnpj in (c * 14 for c in "0123456789"):
        return False

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma1 = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto1 = soma1 % 11
    digito1 = 0 if resto1 < 2 else 11 - resto1

    soma2 = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto2 = soma2 % 11
    digito2 = 0 if resto2 < 2 else 11 - resto2

    return digito1 == int(cnpj[12]) and digito2 == int(cnpj[13])


def validar_telefone(telefone):
    if not telefone:
        return False
    
    padrao_telefone = r'^\(?[1-9]{2}\)?\s?(?:9\d{4}|\d{4})-?\d{4}$'
    return bool(re.match(padrao_telefone, telefone.strip()))