# authenticator_service.py - Autenticacao de usuarios do sistema.

from ..validators.validator import validar_email, validar_cpf, validar_cnpj, validar_senha
from ..managers.database_manager import carregar_database

def _somente_digitos(valor):
    return "".join(filter(str.isdigit, valor))

# Função para realizar o login de um usuário
def login(tipo_usuario, serial_service):
    from ..ui.motorista_ui import menu_motorista
    from ..ui.empresario_ui import menu_empresario
    
    dados = carregar_database()
    usuarios = dados.get("usuarios", {})

    while True:
        email = input("Email: ").strip()
        if validar_email(email):
            break
        print("Email invalido! Por favor, tente novamente.")

    while True:
        senha = input("Senha: ").strip()
        if validar_senha(senha):
            break
        print("Senha invalida! Por favor, tente novamente.")
        return None

    if tipo_usuario == "empresario":
        while True:
            documento = input("Digite o seu CNPJ: ").strip()
            if validar_cnpj(documento):
                break
            print("CNPJ invalido! Por favor, tente novamente.")
    elif tipo_usuario == "motorista":
        while True:
            documento = input("Digite o seu CPF: ").strip()
            if validar_cpf(documento):
                break
            print("CPF invalido! Por favor, tente novamente.")
    else:
        print("Tipo de usuario invalido! Por favor, tente novamente.")
        return None

    documento_informado = _somente_digitos(documento)

    for usuario in usuarios.values():
        documento_banco = _somente_digitos(usuario.get("documento", ""))

        if (
            usuario.get("tipo_usuario") == tipo_usuario
            and usuario.get("email", "").lower() == email.lower()
            and usuario.get("senha") == senha
            and documento_banco == documento_informado
        ):
            try:
                from .service import obter_localizacao_usuario
                obter_localizacao_usuario(usuario["id_usuario"])
            except Exception as erro:
                print(f"[AVISO] Nao foi possivel atualizar a localizacao: {erro}")
            
            print(f"\nBem-vindo {usuario['nome']}!")
            input("Pressione ENTER para continuar...")

            if usuario["tipo_usuario"] == "motorista":
                menu_motorista(serial_service, usuario["id_usuario"])
            elif usuario["tipo_usuario"] == "empresario":
                menu_empresario(serial_service, usuario["id_usuario"])

            return usuario

    print("Login invalido! Por favor, tente novamente.")
    input("Pressione ENTER para continuar...")
    return None
