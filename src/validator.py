# validator.py - Responsável por fornecer funções de validação para os dados de entrada do sistema, como validação de email, senha, CPF, CNPJ, etc. 
import re

def validar_nome(nome):
    return isinstance(nome, str) and len(nome.strip()) > 0

def validar_email(email):
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao_email, email) is not None
   
def validar_senha(senha):
    if len(senha) < 8:
        return False
    tem_letra = re.search(r'[A-Za-z]', senha) is not None
    tem_numero = re.search(r'[0-9]', senha) is not None
    return tem_letra is not None and tem_numero is not None


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    if cpf in (c * 11 for c in "0123456789"):
        return False
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])    

def validar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14:
        return False
    if cnpj in (c * 14 for c in "0123456789"):
        return False
    soma1 = sum(int(cnpj[i]) * (5 - i % 8) for i in range(12))
    digito1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(cnpj[i]) * (6 - i % 8) for i in range(13))
    digito2 = (soma2 * 10 % 11) % 10
    return digito1 == int(cnpj[12]) and digito2 == int(cnpj[13])

def validar_telefone(telefone):
    padrao_telefone = r'^\(?\d{2}\)?[\s-]?\d{4,5}-?\d{4}$'
    return re.match(padrao_telefone, telefone) is not None