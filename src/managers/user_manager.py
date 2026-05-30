# user_manager.py - Gerenciamento e CRUD dos usuários

from .database_manager import carregar_database, atualizar_database
from ..validators.validator import validar_nome, validar_email, validar_senha, validar_cpf, validar_cnpj, validar_telefone
from ..services.service import gerar_id
from datetime import datetime

dados = carregar_database()

# Função para cadastrar um novo usuário (empresário ou motorista)
def cadastrar_usuario(tipo_usuario):
    # Recebe e valida as informações do usuário
    nome = input("Nome: ")
    if not validar_nome(nome):
        print("Nome inválido! Por favor, tente novamente.")
        return
    
    email = input("Email: ")
    if not validar_email(email):
        print("Email inválido! Por favor, tente novamente.")
        return
    
    for usuario in dados["usuarios"].values():
        if usuario["email"] == email:
            print("Email já cadastrado!")
            return
    
    if tipo_usuario == "motorista":
        documento = input("CPF: ")
        if not validar_cpf(documento):
            print("CPF inválido! Por favor, tente novamente.")
            return
    
    elif tipo_usuario == "empresario":
        documento = input("CNPJ: ")
        if not validar_cnpj(documento):
            print("CNPJ inválido! Por favor, tente novamente.")
            return
        
    senha = input("Senha: ")
    if not validar_senha(senha):
        print("Senha inválida! Por favor, tente novamente.")
        return
    
    telefone = input("Telefone: ")
    if not validar_telefone(telefone):
        print("Telefone inválido! Por favor, tente novamente.")
        return

    id_usuario = gerar_id("usuario")

    novo_usuario = {
        "id_usuario": id_usuario,
        "nome": nome,
        "tipo_usuario": tipo_usuario,
        "documento": documento,
        "email": email,
        "senha": senha,
        "telefone": telefone,
        "data_cadastro": datetime.now().isoformat(),
        "historico_reservas": []
    }

    dados["usuarios"][id_usuario] = novo_usuario

    atualizar_database(dados)

    print("Usuário cadastrado com sucesso!")

# Função para atualizar as informações de um usuário existente
def atualizar_usuario(id_usuario, alteracao):
    usuarios = dados.get("usuarios", {})

    # Verifica se o usuário existe no banco de dados
    if id_usuario not in dados["usuarios"]:
        print("Usuário não encontrado!")
        return

    # Obtém as informações do usuário a ser atualizado
    usuario = dados["usuarios"][id_usuario]
    tipo_usuario = usuario["tipo_usuario"]

    # Recebe a nova informação a ser atualizada e valida de acordo com o tipo de alteração
    if alteracao=="nome":
        nova_info=input("Digite o novo nome: ")
        if usuario["nome"]==nova_info:
            print("Escolha um nome diferente do atual")
            return
        if not validar_nome(nova_info):
            print("Nome inválido! Por favor, tente novamente.")
            return
        usuario["nome"] = nova_info
    
    if alteracao=="documento":
        if usuario["documento"]==nova_info:
            print("Escolha um número de documento diferente do atual")
            return
        
        if tipo_usuario=="motorista":
            nova_info=input("CPF: ")
            if usuario["documento"]==nova_info:
                print("Escolha um CPF diferente do atual")
                return 
            if not validar_cpf(nova_info):
                print("CPF inválido! Por favor, tente novamente.")
                return
            
        if tipo_usuario=="empresario":
            nova_info=input("CNPJ: ")
            if usuario["documento"]==nova_info:
                print("Escolha um CNPJ diferente do atual")
                return
            if not validar_cnpj(nova_info):
                print("CNPJ inválido! Por favor, tente novamente.")
                return
        
        usuario["documento"]=nova_info

    if alteracao=="email":
        nova_info=input("Digite um novo email: ")
        if usuario["email"]==nova_info:
            print("Escolha um email diferente do atual")
            return
        if not validar_email(nova_info):
            print("Email inválido! Por favor, tente novamente.")
            return
        if nova_info in [usuario.get("email") for usuario in usuarios.values()]:
                print("Email já cadastrado para outro usuário. Por favor, verifique o email e tente novamente.")
                return
        usuario["email"]=nova_info
    
    if alteracao=="senha":
        nova_info=input("Digite uma nova senha: ")
        if usuario["senha"]==nova_info:
            print("Escolha uma senha diferente da atual")
            return
        if not validar_senha(nova_info):
            print("Senha inválida! Por favor, tente novamente.")
            return
        usuario["senha"]=nova_info
    
    if alteracao=="telefone":
        nova_info=input("Digite um novo telefone: ")
        if usuario["telefone"]==nova_info:
            print("Escolha um telefone diferente do atual")
            return
        if not validar_telefone(nova_info):
            print("Telefone inválido! Por favor, tente novamente.")
            return
        usuario["telefone"]=nova_info

    # Atualiza as informações do usuário no banco de dados
    atualizar_database(dados)

    print("Usuário atualizado com sucesso!")

# Função para visualizar as informações de um usuário específico
def visualizar_usuario(id_usuario):
    usuarios = dados.get("usuarios", {})

    # Verifica se o usuário existe no banco de dados
    if id_usuario not in dados["usuarios"]:
        print("Usuário não encontrado!")
        return

    usuario= usuarios.get(id_usuario)
    # Exibe as informações do usuário de forma formatada
    print("\n====== PERFIL USUÁRIO ======")
    print('Nome: ', usuario['nome'])
    print('Email: ', usuario['email'])
    print('Tipo de usuário: ', usuario['tipo_usuario'])
    print('Documento: ', usuario['documento'])
    print('Telefone: ', usuario['telefone'])
    print("\n============================")

# Função para deletar um usuário do sistema, verificando se o ID do usuário existe no banco de dados antes de realizar a exclusão
def deletar_usuario(id_usuario):

    if id_usuario in dados["usuarios"]:
        del dados["usuarios"][id_usuario]
        atualizar_database(dados)
        print("Usuário removido com sucesso!")
    else:
        print("Usuário não encontrado!")