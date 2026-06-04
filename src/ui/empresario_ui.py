from .geral_ui import menu_principal

def menu_empresario(id_usuario):
    if not id_usuario:
        print("ID do motorista não fornecido. Retornando ao menu principal.")
        menu_principal()
        return
    
    while True:
        
        print("------ Menu do Empresário ------")
        print("1. Gerenciar Unidades")
        print("2. Gerenciar Dispositivos")
        print("3. Ver Dashboard")
        print("4. Sair")
        print("-------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerenciar_unidades(id_usuario)
        elif opcao == "2":
            gerenciar_dispositivos(id_usuario)
        elif opcao == "3":
            menu_dashboard_empresario(id_usuario)
        elif opcao == "4":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_dashboard_empresario(id_usuario):
    from ..services.dashboard import (
        dashboard_empresario, 
        horarios_de_pico, 
        unidades_ativas, 
        relatorio_carregadores, 
        reservas_hoje,
        receita_estimada_mes)
    
    if not id_usuario:
        print("ID do motorista não fornecido. Retornando ao menu principal.")
        menu_principal()
        return
    
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

def gerenciar_unidades(id_usuario): 
    from ..managers.database_manager import carregar_database
    from ..managers.unit_manager import (
        cadastrar_unidade, 
        editar_unidade, 
        listar_unidades, 
        deletar_unidade,
        listar_unidade)
    
    if not id_usuario:
        print("ID do motorista não fornecido. Retornando ao menu principal.")
        menu_principal()
        return
    
    dados = carregar_database()
    
    while True:
        print("------ Suas Unidades ------")
        listar_unidades(id_usuario)
        print("--------------------------------")
        print("1. Visualizar Unidade")
        print("2. Cadastrar Unidade")
        print("3. Voltar")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")
        
        try:
            if opcao == "1":
                unidades = dados.get("unidades", {})

                nome_unidade = input("Unidade que deseja visualizar: ")
                
                id_unidade = next((id for id, unidade in unidades.items() if unidade["nome_unidade"] == nome_unidade), None)
                if id_unidade:
                    listar_unidade(id_unidade)
                else:
                    print("Unidade não encontrada.")
            elif opcao == "2":
                cadastrar_unidade(id_usuario)
            elif opcao == "3":
                return
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except Exception as erro:
            print(f"Aconteceu um erro inesperado: {erro}")