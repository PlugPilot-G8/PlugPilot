# reserve_manager.py - Gerenciamento e CRUD das reservas.

from datetime import datetime, timedelta

from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id


STATUS_AGENDADA = "Agendada"
STATUS_EM_ANDAMENTO = "Em andamento"
STATUS_CONCLUIDA = "Concluida"


def criar_reserva(id_motorista):
    return reservar_carregador(id_motorista)


def reservar_carregador(id_motorista, id_carregador=None):
    dados = carregar_database()
    usuarios = dados.get("usuarios", {})
    unidades = dados.get("unidades", {})
    carregadores = dados.get("carregadores", {})
    reservas = dados.setdefault("reservas", {})

    if id_motorista not in usuarios:
        print("Motorista nao encontrado.")
        return None

    usuario = usuarios[id_motorista]

    if usuario.get("tipo_usuario") != "motorista":
        print("Apenas motoristas podem criar reservas.")
        return None

    if id_carregador:
        if id_carregador not in carregadores:
            print("Carregador nao encontrado.")
            return None
        id_unidade = carregadores[id_carregador]["id_unidade"]
    else:
        id_unidade = input("Digite o ID da unidade: ")

        if id_unidade not in unidades:
            print("Unidade nao encontrada.")
            return None

        id_carregador = input("Digite o ID do carregador: ")

        if id_carregador not in carregadores:
            print("Carregador nao encontrado.")
            return None

    carregador = carregadores[id_carregador]

    if carregador["id_unidade"] != id_unidade:
        print("Esse carregador nao pertence a unidade informada.")
        return None

    if carregador["status_atual"].lower() != "disponivel":
        print("Carregador indisponivel.")
        return None

    agendado_para = input("Digite a data da reserva (AAAA-MM-DD HH:MM): ")
    duracao_minutos = int(input("Digite a duracao da reserva em minutos: "))
    valor_estimado = float(input("Digite o valor estimado da recarga: "))

    id_reserva = gerar_id("reserva")
    reserva = {
        "id_reserva": id_reserva,
        "id_motorista": id_motorista,
        "id_unidade": id_unidade,
        "id_carregador": id_carregador,
        "status_reserva": STATUS_AGENDADA,
        "agendado_para": agendado_para,
        "duracao_minutos": duracao_minutos,
        "valor_estimado": valor_estimado,
        "kwh_consumido": 0.0,
        "data_criacao": datetime.now().isoformat(),
    }

    reservas[id_reserva] = reserva
    usuarios[id_motorista].setdefault("historico_reservas", []).append(id_reserva)

    atualizar_database(dados)
    print(f"Reserva {id_reserva} criada com sucesso!")
    return reserva


def visualizar_reserva(id_reserva):
    dados = carregar_database()
    reserva = dados.get("reservas", {}).get(id_reserva)

    if not reserva:
        print("Reserva nao encontrada.")
        return None

    valor_estimado = reserva.get("valor_estimado", reserva.get("valor_estimated", 0.0))

    print(f"""
================ RESERVA =================

ID Reserva: {reserva['id_reserva']}
Motorista: {reserva['id_motorista']}
Unidade: {reserva['id_unidade']}
Carregador: {reserva['id_carregador']}
Status: {reserva['status_reserva']}
Agendamento: {reserva['agendado_para']}
Duracao: {reserva['duracao_minutos']} minutos
Valor Estimado: R$ {valor_estimado}
kWh Consumido: {reserva['kwh_consumido']}

==========================================
""")


def editar_reserva(id_reserva, alteracao):
    dados = carregar_database()
    reservas = dados.get("reservas", {})
    reserva = reservas.get(id_reserva)

    if not reserva:
        print("Reserva nao encontrada.")
        return

    if alteracao == "status":
        nova_info = input("Digite o novo status (Agendada/Concluida/Cancelada): ")
        campo = "status_reserva"
    elif alteracao == "agendamento":
        nova_info = input("Digite a nova data (AAAA-MM-DD HH:MM): ")
        campo = "agendado_para"
    elif alteracao == "duracao":
        nova_info = int(input("Digite a nova duracao em minutos: "))
        campo = "duracao_minutos"
    elif alteracao == "valor":
        nova_info = float(input("Digite o novo valor estimado: "))
        campo = "valor_estimado"
    elif alteracao == "consumo":
        nova_info = float(input("Digite o consumo em kWh: "))
        campo = "kwh_consumido"
    else:
        print("Alteracao invalida.")
        return None

    if reserva.get(campo) == nova_info:
        print("Escolha um valor diferente.")
        return None

    reserva[campo] = nova_info
    atualizar_database(dados)
    print("Reserva atualizada com sucesso!")
    return reserva


def deletar_reserva(id_reserva):
    dados = carregar_database()
    usuarios = dados.get("usuarios", {})
    reservas = dados.get("reservas", {})
    reserva = reservas.get(id_reserva)

    if not reserva:
        print("Reserva nao encontrada.")
        return None

    id_motorista = reserva["id_motorista"]

    if id_motorista in usuarios:
        historico = usuarios[id_motorista].setdefault("historico_reservas", [])
        if id_reserva in historico:
            historico.remove(id_reserva)

    del reservas[id_reserva]
    atualizar_database(dados)
    print(f"Reserva {id_reserva} deletada com sucesso!")
    return reserva


def _converter_data_reserva(data_texto):
    if not data_texto:
        return None

    data_texto = data_texto.strip()
    formatos = [
        "%Y-%m-%d %H:%M",
        "%Y %m %d %H:%M",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%d/%m/%Y %H:%M",
    ]

    for formato in formatos:
        try:
            return datetime.strptime(data_texto, formato)
        except ValueError:
            continue

    partes = data_texto.split()
    if len(partes) >= 4:
        data_corrigida = f"{partes[0]}-{partes[1]}-{partes[2]} {partes[3]}"
        return datetime.strptime(data_corrigida, "%Y-%m-%d %H:%M")

    raise ValueError(f"Formato de data invalido: '{data_texto}'. Use AAAA-MM-DD HH:MM")


def buscar_reserva_ativa_por_carregador(id_carregador):
    dados = carregar_database()
    agora = datetime.now()

    for reserva in dados.get("reservas", {}).values():
        if reserva["id_carregador"] != id_carregador:
            continue

        if reserva["status_reserva"] != STATUS_AGENDADA:
            continue

        inicio = _converter_data_reserva(reserva["agendado_para"])
        fim = inicio + timedelta(minutes=reserva["duracao_minutos"])

        if inicio <= agora <= fim:
            return reserva

    return None


def carregador_esta_reservado(id_carregador):
    return buscar_reserva_ativa_por_carregador(id_carregador) is not None


def obter_comando_estado_carregador(id_carregador):
    if carregador_esta_reservado(id_carregador):
        return f"RESERVED:{id_carregador}"

    return f"FREE:{id_carregador}"

def validar_liberacao_por_codigo(
    id_carregador,
    id_motorista,
    codigo_digitado,
    codigos_ativos,
):
    reserva = buscar_reserva_ativa_por_carregador(id_carregador)

    if not reserva:
        return True, "Carregador livre. Uso permitido."

    if reserva["id_motorista"] != id_motorista:
        return False, "Este carregador esta reservado para outro usuario."

    codigo_info = codigos_ativos.get(id_carregador)

    if not codigo_info:
        return False, "Nenhum codigo ativo para este carregador."

    if datetime.now() > codigo_info["expira_em"]:
        return False, "Codigo expirado."

    if codigo_info["codigo"] != codigo_digitado:
        return False, "Codigo incorreto."

    dados = carregar_database()
    reserva_banco = dados.get("reservas", {}).get(reserva["id_reserva"])

    if reserva_banco:
        reserva_banco["status_reserva"] = STATUS_EM_ANDAMENTO
        reserva_banco["inicio_recarga"] = datetime.now().isoformat()
        atualizar_database(dados)

    return True, "Reserva validada. Uso permitido."
