# geral_ui.py - Menu Principal e Navegação de Fluxo do Sistema

from ..managers.user_manager import cadastrar_usuario
from ..services.authenticator_service import login

def menu_principal(serial_service=None):
    while True:
        print("\n------ Menu Principal - PlugPilot! ------")
        print("1. Login")
        print("2. Cadastrar")
        print("3. Sair")
        print("-----------------------------------------")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            login_menu(serial_service)
        elif opcao == "2":
            cadastro_menu(serial_service)
        elif opcao == "3":
            print("Saindo do PlugPilot!... Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def login_menu(serial_service=None):
    while True:
        print("\n------ Menu de Login ------")
        print("1. Login Empresário")
        print("2. Login Motorista")
        print("3. Voltar ao Menu Principal")
        print("---------------------------")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            login("empresario", serial_service)
            return
        elif opcao == "2":
            login("motorista", serial_service)
            return
        elif opcao == "3":
            break 
        else:
            print("Opção inválida. Por favor, tente novamente.")

def cadastro_menu(serial_service=None):
    while True:
        print("\n------ Menu de Cadastro ------")
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
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")