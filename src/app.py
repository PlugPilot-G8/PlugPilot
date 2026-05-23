# app.py - Responsável por gerenciar o menu principal, login e cadastro.
from .database_manager import carregar_database 

dados = carregar_database()
def menu_principal():
    while True:
        print("------ Menu Principal - PlugPilot! ------")
        print("1. Login")
        print("2. Cadastrar")
        print("3. Sair")
        print("-----------------------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Opção de Login selecionada.")
            login_menu()
        elif opcao == "2":
            print("Opção de Cadastro selecionada.")
            cadastro_menu()
        elif opcao == "3":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def cadastro_menu():
    from .service import cadastrar_usuario
    while True:
        print("------ Menu de Cadastro ------")
        print("1. Cadastrar Empresário")
        print("2. Cadastrar Motorista")
        print("3. Voltar ao Menu Principal")
        print("------------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Cadastro de Empresário selecionado.")
            # Chama a função de cadastro para empresário
            cadastrar_usuario("empresario")
            return
        elif opcao == "2":
            print("Cadastro de Motorista selecionado.")
            # Chama a função de cadastro para motorista
            cadastrar_usuario("motorista")
            return
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def login_menu():
    from .service import login
    while True:
        print("------ Menu de Login ------")
        print("1. Login Empresário")
        print("2. Login Motorista")
        print("3. Voltar ao Menu Principal")
        print("---------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Login de Empresário selecionado.")
            # Chama a função de login para empresário
            login("empresario") 
            return 
        elif opcao == "2":      
            print("Login de Motorista selecionado.")
            # Chama a função de login para motorista
            login("motorista")
            return
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_motorista():
    while True:
        print("------ Menu do Motorista ------")
        print("1. Visualizar Unidades Disponíveis")
        print("2. Gerenciar Reservas")
        print("3. Sair")
        print("------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Visualizar Unidades Disponíveis selecionado.")
            unidades_disponiveis()
        elif opcao == "2":
            print("Gerenciar Reservas selecionado.")
            # Chama a função para gerenciar reservas
            return
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_empresario():
    while True:
        print("------ Menu do Empresário ------")
        print("1. Gerenciar Unidades")
        print("2. Gerenciar Dispositivos")
        print("3. Sair")
        print("-------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Gerenciar Unidades selecionado.")
            # Chama a função para gerenciar unidades
            return
        elif opcao == "2":
            print("Gerenciar Dispositivos selecionado.")
            # Chama a função para gerenciar dispositivos
            return
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

unidades = dados.get("unidades")
        
def unidades_disponiveis():
    from .service import visualizar_carregadores
    print("------Estações disponiveis------")
    for i in range(len(unidades)):
        unidade_id = list(unidades.keys())[i]
        unidade = unidades.get(unidade_id)
        nome = unidade.get("nome_unidade")
        print(f"{i+1}.",nome)
    print("--------------------------------")

    opcao = int(input("Escolha o que você deseja: "))
    
    unidade_id = list(unidades.keys())[opcao - 1]

    unidade_escolhida = unidades[unidade_id]

    print("Você escolheu:", unidade_escolhida["nome_unidade"])
     
    visualizar_carregadores()

