from ..managers.database_manager import carregar_database 

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
    from ..managers.user_manager import cadastrar_usuario
    while True:
        print("------ Menu de Cadastro ------")
        print("1. Cadastrar Empresário")
        print("2. Cadastrar Motorista")
        print("3. Voltar ao Menu Principal")
        print("------------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_usuario("empresario")
            return
        elif opcao == "2":
            cadastrar_usuario("motorista")
            return
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def login_menu():
    from ..services.authenticator_service import login
    while True:
        print("------ Menu de Login ------")
        print("1. Login Empresário")
        print("2. Login Motorista")
        print("3. Voltar ao Menu Principal")
        print("---------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            login("empresario")
            return
        elif opcao == "2":
            login("motorista")
            return
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")