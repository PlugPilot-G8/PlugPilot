from .geral_ui import menu_principal
from ..services.dashboard import dashboard_empresario, horarios_de_pico
from ..managers.unit_manager import listar_unidades, cadastrar_unidade, deletar_unidade 
from ..managers.chager_manager import listar_carregadores, cadastrar_carregador, deletar_carregador


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
            gerenciar_unidades()
        elif opcao == "2":
            print("Gerenciar Dispositivos selecionado.")
            gerenciar_dispositivos()
        elif opcao == "3":
            id_usuario = input("Digite o ID do empresário: ")
            menu_dashboard_empresario(id_usuario)
        elif opcao == "4":
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

def gerenciar_unidades(): 
    print("Gerenciar Unidades selecionado.")
    
    while True:
        print("------ Gerenciar Unidades ------")
        print("1. Listar Unidades")
        print("2. Cadastrar Unidade")
        print("3. Deletar Unidade")
        print("4. Voltar")
        print("--------------------------------")

        op = input("Escolha uma opção: ")
        try:
            if op == "1":
                listar_unidades()
            elif op == "2":
                cadastrar_unidade()
            elif op == "3":
                deletar_unidade()
            elif op == "4":
                return
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except Exception as erro:
            print(f"Aconteceu um erro inesperado: {erro}")
        input("Aperte Enter para continuar: ")
    

def gerenciar_dispositivos():
    print("Gerenciar Dispositivos selecionado.")
    
    while True:
        if not listar_carregadores():
            print("Nenhum carregador cadastrado. Por favor, cadastre um carregador primeiro.")
            cadastrar_carregador()
            continue
        print("------ Gerenciar Dispositivos ------")
        print("1. Listar Dispositivos") 
        print("2. Cadastrar Dispositivo")
        print("3. Deletar Dispositivo")
        print("4. Voltar")
        print("-----------------------------------")
        
        op = input("Escolha uma opção: ")
        
        try:
            if op == "1":
                listar_carregadores()
            elif op == "2":
                cadastrar_carregador()
            elif op == "3":
                deletar_carregador()
            elif op == "4":
                return
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except Exception as erro:
            print(f"Aconteceu um erro inesperado: {erro}")
        input("Aperte Enter para continuar: ")