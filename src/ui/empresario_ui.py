from .geral_ui import menu_principal

def menu_empresario(serial_service, id_usuario):
    if not id_usuario:
        print("ID do empresário não fornecido. Retornando ao menu principal.")
        menu_principal(serial_service)
        return
    
    while True:
        print("\n------ Menu do Empresário ------")
        print("1. Gerenciar Unidades")
        print("2. Ver Dashboard")
        print("3. Visualizar Perfil")
        print("4. Sair")
        print("-------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerenciar_unidades(serial_service, id_usuario)
        elif opcao == "2":
            menu_dashboard_empresario(serial_service, id_usuario)
        elif opcao == "3":
            from ..managers.user_manager import visualizar_usuario
            visualizar_usuario(id_usuario)
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_dashboard_empresario(serial_service, id_usuario):
    from ..services.serial_service import (
        dashboard_empresario, 
        horarios_de_pico, 
        unidades_ativas, 
        relatorio_carregadores, 
        reservas_hoje,
        receita_estimada_mes
    )
    
    if not id_usuario:
        print("ID do empresário não fornecido. Retornando ao menu principal.")
        menu_principal(serial_service)
        return
    
    while True:
        print("\n------ Dashboard do Empresário ------")
        print(f"Unidades ativas: {unidades_ativas(id_usuario)}")
        relatorio_carregadores(id_usuario)
        print(f"Reservas hoje: {reservas_hoje(id_usuario)}")
        print(f"Receita estimada: R$ {receita_estimada_mes(id_usuario):.2f}")
        print("-------------------------------------")
        print("1. Taxa de Ocupação Semanal")
        print("2. Horários de Pico")
        print("3. Voltar")
        print("-------------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Exibindo Taxa de Uso Semanal...")
            dashboard_empresario(id_usuario)
        elif opcao == "2":
            print("Exibindo Horários de Pico...")
            horarios_de_pico(id_usuario)
        elif opcao == "3":
            return
        else:
            print("Opção inválida. Por favor, tente novamente.")

def gerenciar_unidades(serial_service, id_usuario): 
    from ..managers.unit_manager import (
        cadastrar_unidade, 
        listar_unidades, 
        listar_unidade,
    )
    
    from ..managers.database_manager import conectar
    
    if not id_usuario:
        print("ID do empresário não fornecido. Retornando ao menu principal.")
        menu_principal(serial_service)
        return
    
    while True:
        print("\n------ Suas Unidades ------")
        listar_unidades(id_usuario)
        print("--------------------------------")
        print("1. Visualizar Unidade")
        print("2. Cadastrar Unidade")
        print("3. Voltar")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")
        
        try:
            if opcao == "1":
                nome_unidade = input("Unidade que deseja visualizar: ").strip()
                
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id_unidade FROM unidades WHERE nome_unidade = ? AND id_dono = ?", 
                    (nome_unidade, id_usuario)
                )
                row = cursor.fetchone()
                conn.close()

                if row:
                    listar_unidade(id_usuario, row["id_unidade"])
                else:
                    print("Unidade não encontrada ou não pertence a você.")
                    
            elif opcao == "2":
                cadastrar_unidade(id_usuario)
            elif opcao == "3":
                return
            else:
                print("Opção inválida. Por favor, tente novamente.")
        except Exception as erro:
            print(f"Aconteceu um erro inesperado: {erro}")