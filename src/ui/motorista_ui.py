# motorista_ui.py - Interface do Motorista e Gerenciamento de Reservas via SQLite

from .geral_ui import menu_principal
from ..managers.database_manager import conectar

def menu_motorista(serial_service, id_usuario):
    from ..managers.unit_manager import listar_unidades_proximas, listar_unidade
    
    if not id_usuario:
        print("ID do motorista não fornecido. Retornando ao menu principal.")
        return
    
    while True:
        print("\n------ Menu do Motorista ------")
        listar_unidades_proximas(id_usuario)
        print("------------------------------")
        print("1. Visualizar Unidade")
        print("2. Gerenciar Reservas")
        print("3. Sair")
        print("------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome_unidade = input("Unidade que deseja visualizar: ").strip()
            
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_unidade FROM unidades WHERE LOWER(nome_unidade) = LOWER(?)", (nome_unidade,))
            row = cursor.fetchone()
            conn.close()

            if row:
                listar_unidade(id_usuario, row["id_unidade"], serial_service)
            else:
                print("Unidade não encontrada.")
                
        elif opcao == "2":
            menu_reservas(serial_service, id_usuario)
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


def menu_reservas(serial_service, id_motorista):
    from ..managers.reserve_manager import (
        reservar_carregador,
        visualizar_reserva,
        editar_reserva,
        deletar_reserva,
        validar_liberacao_por_codigo,
        obter_comando_estado_carregador
    )
    from ..managers.charger_manager import atualizar_status_carregador

    def sincronizar_lcd(id_carregador, comando=None):
        if not serial_service:
            print("[SERIAL] Servico serial indisponivel.")
            return

        if comando is None:
            comando = obter_comando_estado_carregador(id_carregador)

        serial_service.enviar_comando(comando)

    while True:
        print("\n------ Gerenciar Reservas ------")
        print("1. Criar Reserva")
        print("2. Iniciar Recarga")
        print("3. Visualizar Reserva")
        print("4. Editar Reserva")
        print("5. Deletar Reserva")
        print("6. Voltar")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            reserva = reservar_carregador(id_motorista)
            if reserva and serial_service:
                id_carregador = reserva["id_carregador"]
                atualizar_status_carregador(id_carregador, "Reservado")
                sincronizar_lcd(id_carregador, f"RESERVED:{id_carregador}")

        elif opcao == "2":
            if not serial_service:
                print("[SERIAL] Servico serial indisponivel.")
                continue

            id_carregador = input("Digite o ID do carregador: ").strip() or "chg_001"
            codigo = input("Digite o codigo exibido no LCD: ").strip()

            sucesso = serial_service.liberar_por_codigo(
                id_carregador=id_carregador,
                id_motorista=id_motorista,
                codigo_digitado=codigo,
                validar_liberacao_callback=validar_liberacao_por_codigo
            )

            if sucesso:
                print("[PlugPilot] Carregador liberado.")
            else:
                print("[PlugPilot] Codigo incorreto, expirado ou reserva invalida.")

        elif opcao == "3":
            id_reserva = input("Digite o ID da reserva: ")
            visualizar_reserva(id_reserva)

        elif opcao == "4":
            id_reserva = input("Digite o ID da reserva: ")

            print("\nO que deseja alterar?")
            print("1. Status")
            print("2. Agendamento")
            print("3. Duração")
            print("4. Valor")
            print("5. Consumo")

            campo = input("Escolha: ")
            reserva_atualizada = None

            if campo == "1":
                reserva_atualizada = editar_reserva(id_reserva, "status")
            elif campo == "2":
                reserva_atualizada = editar_reserva(id_reserva, "agendamento")
            elif campo == "3":
                reserva_atualizada = editar_reserva(id_reserva, "duracao")
            elif campo == "4":
                reserva_atualizada = editar_reserva(id_reserva, "valor")
            elif campo == "5":
                reserva_atualizada = editar_reserva(id_reserva, "consumo")
            else:
                print("Opção inválida.")

            if reserva_atualizada:
                sincronizar_lcd(reserva_atualizada["id_carregador"])

        elif opcao == "5":
            id_reserva = input("Digite o ID da reserva: ")
            reserva_deletada = deletar_reserva(id_reserva)
            if reserva_deletada:
                sincronizar_lcd(reserva_deletada["id_carregador"])

        elif opcao == "6":
            break
        else:
            print("Opção inválida.")

def unidades_disponiveis():
    from ..managers.unit_manager import visualizar_unidade
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_unidade, nome_unidade FROM unidades WHERE LOWER(status) = 'ativa'")
    unidades = cursor.fetchall()
    conn.close()

    print("\n------ Estações Disponíveis ------")
    if not unidades:
        print("Nenhuma unidade ativa encontrada.")
        return

    for idx, unidade in enumerate(unidades):
        print(f"{idx + 1}. {unidade['nome_unidade']}")
    print("--------------------------------")

    try:
        opcao = int(input("Escolha o que você deseja: "))
        if 1 <= opcao <= len(unidades):
            unidade_escolhida = unidades[opcao - 1]
            print("Você escolheu:", unidade_escolhida["nome_unidade"])
            visualizar_unidade(unidade_escolhida["id_unidade"])
        else:
            print("Opção fora do intervalo disponível.")
    except ValueError:
        print("Por favor, digite um número válido.")