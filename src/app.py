# app.py - Responsável por gerenciar o menu principal, login e cadastro.

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
    while True:
        print("------ Menu de Cadastro ------")
        print("1. Cadastrar Empresário")
        print("2. Cadastrar Motorista")
        print("3. Voltar ao Menu Principal")
        print("------------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Cadastro de Empresário selecionado.")
            # Aqui você pode chamar a função de cadastro para empresário
        elif opcao == "2":
            print("Cadastro de Motorista selecionado.")
            # Aqui você pode chamar a função de cadastro para motorista
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def login_menu():
    while True:
        print("------ Menu de Login ------")
        print("1. Login Empresário")
        print("2. Login Motorista")
        print("3. Voltar ao Menu Principal")
        print("---------------------------")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Login de Empresário selecionado.")
            # Aqui você pode chamar a função de login para empresário
        elif opcao == "2":
            print("Login de Motorista selecionado.")
            # Aqui você pode chamar a função de login para motorista
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")