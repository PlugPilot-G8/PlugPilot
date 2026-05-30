#authenticator.py - Responsável por fornecer funções de autenticação para o sistema, como login, logout, verificação de sessão, etc.
from ..validators.validator import validar_email, validar_cpf, validar_cnpj, validar_senha
from ..managers.database_manager import carregar_database
from ..ui.terminal_ui import menu_motorista, menu_empresario

dados = carregar_database()

# Função para realizar o login de um usuário
def login(tipo_usuario):
    usuarios = dados.get("usuarios", {})
    # Recebe e valida as informações do usuário
    while True:
        email = input("Email: ")
        if not validar_email(email):
            print("Email inválido! Por favor, tente novamente.")
        else:
            break
    
    while True:
        senha = input("Senha: ")
        if not validar_senha(senha):
            print("Senha inválida! Por favor, tente novamente.")
            return
        else:
            break
    
    if tipo_usuario=="empresario":
        while True:
            documento=input("Digite o seu CNPJ: ")
            if not validar_cnpj(documento):
                print("CNPJ inválido! Por favor, tente novamente.")
            else:
                break
    elif tipo_usuario == "motorista":
        while True:
            documento=input("Digite o seu CPF: ")
            if not validar_cpf(documento):
                print("CPF inválido! Por favor, tente novamente.")
            else:
                break
    else:
        print("Tipo de usuário inválido! Por favor, tente novamente.")
        return

    # Verifica as credenciais do usuário no banco de dados, comparando o email, senha e documento fornecidos com os registros existentes
    for usuario in usuarios.values():
        if usuario["email"] == email and usuario["senha"] == senha and usuario["documento"] == documento:

            print(f"\nBem-vindo {usuario['nome']}!")
            if usuario["tipo_usuario"] == "motorista":
                input("Pressione ENTER para continuar...")
                menu_motorista()
            elif usuario["tipo_usuario"] == "empresario":
                input("Pressione ENTER para continuar...")
                menu_empresario()
        else:
            print(f"Login Inválido! Por favor, tente novamente.")
    input("Pressione ENTER para continuar...")
    return None