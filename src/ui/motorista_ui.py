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
        print("3. Visualizar Perfil")
        print("4. Sair")
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
            from ..managers.user_manager import visualizar_usuario
            visualizar_usuario(id_usuario)      
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


def menu_reservas(serial_service, id_motorista):
    from ..managers.reserve_manager import (
        visualizar_reserva,
        listar_reservas,
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
        print("\n------ Minhas Reservas ------")
        listar_reservas(id_motorista)
        print("\n------ Gerenciar Reservas ------")
        print("1. Visualizar Reserva")
        print("2. Voltar")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_reserva = input("ID da reserva: ")
            visualizar_reserva(id_reserva, id_motorista, serial_service)
            
        elif opcao == "2":
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