from ..managers.database_manager import dados
from .geral_ui import menu_principal

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
            id_usuario = input("Digite o ID do motorista: ")
            menu_reservas(id_usuario)
        elif opcao == "3":
            menu_principal()
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

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

def unidades_disponiveis():
    from ..managers.unit_manager import visualizar_unidade
    
    unidades = dados.get("unidades")

    print("------Estações disponiveis------")
    if not unidades:
            print("Nenhuma unidade cadastrada.")
            return
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