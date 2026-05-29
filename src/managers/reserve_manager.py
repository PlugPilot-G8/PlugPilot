# reserve_manager.py - Gerenciamento e CRUD das reservas

from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id
from datetime import datetime

dados = carregar_database()

reservas = dados.setdefault("reservas", {})

def criar_reserva(id_motorista):
    usuarios = dados.get("usuarios", {})
    unidades = dados.get("unidades", {})
    carregadores = dados.get("carregadores", {})

    if id_motorista not in usuarios:
        print("Motorista não encontrado.")
        return

    usuario = usuarios[id_motorista]

    if usuario["tipo_usuario"] != "motorista":
        print("Apenas motoristas podem criar reservas.")
        return

    id_unidade = input("Digite o ID da unidade: ")

    if id_unidade not in unidades:
        print("Unidade não encontrada.")
        return

    id_carregador = input("Digite o ID do carregador: ")

    if id_carregador not in carregadores:
        print("Carregador não encontrado.")
        return

    carregador = carregadores[id_carregador]

    # Verifica se carregador pertence à unidade
    if carregador["id_unidade"] != id_unidade:
        print("Esse carregador não pertence à unidade informada.")
        return

    # Verifica disponibilidade
    if carregador["status_atual"].lower() != "disponivel":
        print("Carregador indisponível.")
        return

    agendado_para = input("Digite a data da reserva (AAAA-MM-DD HH:MM): ")

    duracao_minutos = int(input("Digite a duração da reserva em minutos: "))

    valor_estimado = float(input("Digite o valor estimado da recarga: "))

    id_reserva = gerar_id("reserva")

    reservas.update({
        id_reserva: {
            "id_reserva": id_reserva,
            "id_motorista": id_motorista,
            "id_unidade": id_unidade,
            "id_carregador": id_carregador,
            "status_reserva": "Agendada",
            "agendado_para": agendado_para,
            "duracao_minutos": duracao_minutos,
            "valor_estimado": valor_estimado,
            "kwh_consumido": 0.0,
            "data_criacao": datetime.now().isoformat()
        }
    })

    # adiciona reserva ao histórico do usuário
    usuarios[id_motorista]["historico_reservas"].append(id_reserva)

    atualizar_database(dados)

    print(f"Reserva {id_reserva} criada com sucesso!")


def visualizar_reserva(id_reserva):

    reserva = reservas.get(id_reserva)

    if reserva:

        print(f"""
================ RESERVA =================

ID Reserva: {reserva['id_reserva']}
Motorista: {reserva['id_motorista']}
Unidade: {reserva['id_unidade']}
Carregador: {reserva['id_carregador']}
Status: {reserva['status_reserva']}
Agendamento: {reserva['agendado_para']}
Duração: {reserva['duracao_minutos']} minutos
Valor Estimado: R$ {reserva['valor_estimado']}
kWh Consumido: {reserva['kwh_consumido']}

==========================================
""")

    else:
        print("Reserva não encontrada.")


def editar_reserva(id_reserva, alteracao):

    reserva = reservas.get(id_reserva)

    if not reserva:
        print("Reserva não encontrada.")
        return

    if alteracao == "status":

        novo_status = input(
            "Digite o novo status (Agendada/Concluida/Cancelada): "
        )

        if novo_status == reserva["status_reserva"]:
            print("Escolha um status diferente.")
            return

        reserva["status_reserva"] = novo_status

    elif alteracao == "agendamento":

        novo_agendamento = input(
            "Digite a nova data (AAAA-MM-DD HH:MM): "
        )

        if novo_agendamento == reserva["agendado_para"]:
            print("Escolha uma data diferente.")
            return

        reserva["agendado_para"] = novo_agendamento

    elif alteracao == "duracao":

        nova_duracao = int(
            input("Digite a nova duração em minutos: ")
        )

        if nova_duracao == reserva["duracao_minutos"]:
            print("Escolha uma duração diferente.")
            return

        reserva["duracao_minutos"] = nova_duracao

    elif alteracao == "valor":

        novo_valor = float(
            input("Digite o novo valor estimado: ")
        )

        if novo_valor == reserva["valor_estimado"]:
            print("Escolha um valor diferente.")
            return

        reserva["valor_estimado"] = novo_valor

    elif alteracao == "consumo":

        novo_consumo = float(
            input("Digite o consumo em kWh: ")
        )

        if novo_consumo == reserva["kwh_consumido"]:
            print("Escolha um valor diferente.")
            return

        reserva["kwh_consumido"] = novo_consumo

    else:
        print("Alteração inválida.")
        return

    atualizar_database(dados)

    print("Reserva atualizada com sucesso!")


def deletar_reserva(id_reserva):
    usuarios = dados.get("usuarios", {})

    reserva = reservas.get(id_reserva)

    if not reserva:
        print("Reserva não encontrada.")
        return

    id_motorista = reserva["id_motorista"]

    # remove do histórico do usuário
    if id_motorista in usuarios:

        historico = usuarios[id_motorista]["historico_reservas"]

        if id_reserva in historico:
            historico.remove(id_reserva)

    del reservas[id_reserva]

    atualizar_database(dados)

    print(f"Reserva {id_reserva} deletada com sucesso!")