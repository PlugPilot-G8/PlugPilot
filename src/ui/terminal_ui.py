# terminal_ui.py - Responsável por gerenciar o menu principal, login e cadastro.
from ..managers.database_manager import carregar_database
from ..services.dashboard import dashboard_empresario, horarios_de_pico, unidades_ativas

from ..managers.database_manager import carregar_database 

# Carrega a base de dados do sistema para ser utilizada na função de visualização de unidades
dados = carregar_database()

# Função para exibir o menu principal do sistema (login, cadastro)


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

# Função para exibir o menu de cadastro, permitindo ao usuário escolher entre cadastrar como empresário ou motorista


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

# Função para exibir o menu de login, permitindo ao usuário escolher entre login como empresário ou motorista


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

# Função para exibir o menu do motorista, permitindo ao motorista visualizar unidades disponíveis e gerenciar reservas

def menu_motorista():
    while True:
        print("------ Menu do Motorista ------")
        print("1. Visualizar Unidades Disponíveis")
        print("2. Gerenciar Reservas")
        print("3. Sair")
        print("------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            unidades_disponiveis()
        elif opcao == "2":
            menu_reservas()
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_dashboard_empresario(id_usuario):
    from ..services.dashboard import  unidades_ativas, relatorio_carregadores,reservas_hoje,receita_estimada_mes

    
    while True:
        print("------ Dashboard do Empresário ------")
        print(f"Unidades ativas: {unidades_ativas(id_usuario)}")
        relatorio_carregadores(id_usuario)
        print(f"Reservas hoje: {reservas_hoje()}")
        print(f"Receita estimada: R$ {receita_estimada_mes(id_usuario):.2f}")
        print("1. Taxa de Ocupação Semanal")
        print("2. Horários de Pico")
        print("3. Voltar")
        print("-------------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Exibindo Taxa de Uso Semanal...")
            dashboard_empresario()
        elif opcao == "2":
            print("Exibindo Horários de Pico...")
            horarios_de_pico()
        elif opcao == "3":
            return
        else:
            print("Opção inválida. Por favor, tente novamente.")

# Função para exibir o menu do empresário, permitindo ao empresário gerenciar suas unidades e dispositivos

def menu_empresario():
    while True:
        print("------ Menu do Empresário ------")
        print("1. Gerenciar Unidades")
        print("2. Gerenciar Dispositivos")
        print("3. Ver Dashboard")
        print("4. Sair")
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
            id_usuario = input("Digite o ID do empresário: ")
            menu_dashboard_empresario(id_usuario)
        elif opcao == "4":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

# Função para exibir as unidades disponíveis para reserva, permitindo ao motorista escolher uma unidade e visualizar seus carregadores

def unidades_disponiveis():
    from ..managers.unit_manager import visualizar_unidade
    
    unidades = dados.get("unidades")

    print("------Estações disponiveis------")
    for i in range(len(unidades)):
        unidade_id = list(unidades.keys())[i]
        unidade = unidades.get(unidade_id)
        nome = unidade.get("nome_unidade")
        print(f"{i+1}.", nome)
    print("--------------------------------")

    opcao = int(input("Escolha o que você deseja: "))

    unidade_id = list(unidades.keys())[opcao - 1]

    unidade_escolhida = unidades[unidade_id]

    print("Você escolheu:", unidade_escolhida["nome_unidade"])

    visualizar_unidade(unidade_escolhida["id_unidade"])

def menu_reservas(id_motorista):
    from ..managers.reserve_manager import (
        criar_reserva,
        visualizar_reserva,
        editar_reserva,
        deletar_reserva
    )

    while True:
        print("\n------ Gerenciar Reservas ------")
        print("1. Criar Reserva")
        print("2. Visualizar Reserva")
        print("3. Editar Reserva")
        print("4. Deletar Reserva")
        print("5. Voltar")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_reserva(id_motorista)

        elif opcao == "2":
            id_reserva = input("Digite o ID da reserva: ")
            visualizar_reserva(id_reserva)

        elif opcao == "3":
            id_reserva = input("Digite o ID da reserva: ")

            print("\nO que deseja alterar?")
            print("1. Status")
            print("2. Agendamento")
            print("3. Duração")
            print("4. Valor")
            print("5. Consumo")

            campo = input("Escolha: ")

            if campo == "1":
                editar_reserva(id_reserva, "status")
            elif campo == "2":
                editar_reserva(id_reserva, "agendamento")
            elif campo == "3":
                editar_reserva(id_reserva, "duracao")
            elif campo == "4":
                editar_reserva(id_reserva, "valor")
            elif campo == "5":
                editar_reserva(id_reserva, "consumo")
            else:
                print("Opção inválida.")

        elif opcao == "4":
            id_reserva = input("Digite o ID da reserva: ")
            deletar_reserva(id_reserva)

        elif opcao == "5":
            break

        else:
            print("Opção inválida.")