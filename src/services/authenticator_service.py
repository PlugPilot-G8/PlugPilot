# authenticator_service.py - Autenticacao de usuarios do sistema via SQLite.

from ..validators.validator import validar_email, validar_cpf, validar_cnpj, validar_senha, criptografar_senha
from ..services.service import obter_localizacao_usuario
from ..managers.database_manager import conectar

def somente_digitos(valor):
    return "".join(filter(str.isdigit, valor))

def login(tipo_usuario, serial_service):
    from ..ui.motorista_ui import menu_motorista
    from ..ui.empresario_ui import menu_empresario
    
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

    documento_informado = somente_digitos(documento)
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios 
        WHERE LOWER(email) = LOWER(?) 
          AND senha = ? 
          AND tipo_usuario = ?
    """, (email, criptografar_senha(senha), tipo_usuario))
    
    usuario_row = cursor.fetchone()
    conn.close()

    if usuario_row:
        documento_banco = somente_digitos(usuario_row["documento"] if usuario_row["documento"] is not None else "")
        
        if documento_banco == documento_informado:
            usuario = dict(usuario_row)
            
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