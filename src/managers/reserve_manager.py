# reserve_manager.py - Gerenciamento e CRUD das reservas via SQLite.

from datetime import datetime
from .database_manager import conectar
from ..services.service import gerar_id

STATUS_AGENDADA = "Agendada"
STATUS_EM_ANDAMENTO = "Em andamento"
STATUS_CONCLUIDA = "Concluida"

def criar_reserva(id_motorista):
    return reservar_carregador(id_motorista)

def reservar_carregador(id_motorista, id_carregador=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id_usuario = ?", (id_motorista,))
    usuario = cursor.fetchone()
    if not usuario:
        print("Motorista nao encontrado.")
        conn.close()
        return None

    if usuario["tipo_usuario"] != "motorista":
        print("Apenas motoristas podem criar reservas.")
        conn.close()
        return None

    if id_carregador:
        cursor.execute("SELECT id_unidade, status_atual FROM carregadores WHERE id_carregador = ?", (id_carregador,))
        carregador = cursor.fetchone()
        if not carregador:
            print("Carregador nao encontrado.")
            conn.close()
            return None
        id_unidade = carregador["id_unidade"]
        
    else:
        id_unidade = input("Digite o ID da unidade: ")
        cursor.execute("SELECT id_unidade FROM unidades WHERE id_unidade = ?", (id_unidade,))
        if not cursor.fetchone():
            print("Unidade nao encontrada.")
            conn.close()
            return None

        id_carregador = input("Digite o ID do carregador: ")
        
        cursor.execute("SELECT id_unidade, status_atual FROM carregadores WHERE id_carregador = ?", (id_carregador,))
        carregador = cursor.fetchone()
        if not carregador:
            print("Carregador nao encontrado.")
            conn.close()
            return None

    if carregador["id_unidade"] != id_unidade:
        print("Esse carregador nao pertence a unidade informada.")
        conn.close()
        return None

    if carregador["status_atual"].lower() != "disponivel":
        print("Carregador indisponivel.")
        conn.close()
        return None

    agendado_para_input = input("Digite a data da reserva (AAAA-MM-DD HH:MM): ")
    
    try:
        data_formatada = datetime.strptime(agendado_para_input.strip(), "%Y-%m-%d %H:%M").isoformat()
    except ValueError:
        print("Formato de data invalido. Use AAAA-MM-DD HH:MM")
        conn.close()
        return None

    duracao_minutos = int(input("Digite a duracao da reserva em minutos: "))
    valor_estimado = float(input("Digite o valor estimado da recarga: "))

    id_reserva = gerar_id("reserva")

    cursor.execute("""
        INSERT INTO reservas (
            id_reserva, id_motorista, id_unidade, id_carregador, 
            status_reserva, agendado_para, duracao_minutos, valor_estimado, kwh_consumido
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_reserva, id_motorista, id_unidade, id_carregador,
        STATUS_AGENDADA, data_formatada, duracao_minutos, valor_estimado, 0.0
    ))

    conn.commit()
    
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva_criada = dict(cursor.fetchone())
    conn.close()

    print(f"Reserva {id_reserva} criada com sucesso!")
    return reserva_criada


def visualizar_reserva(id_reserva):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva = cursor.fetchone()
    conn.close()

    if not reserva:
        print("Reserva nao encontrada.")
        return None

    print(f"""
================ RESERVA =================

ID Reserva: {reserva['id_reserva']}
Motorista: {reserva['id_motorista']}
Unidade: {reserva['id_unidade']}
Carregador: {reserva['id_carregador']}
Status: {reserva['status_reserva']}
Agendamento: {reserva['agendado_para']}
Duracao: {reserva['duracao_minutos']} minutos
Valor Estimado: R$ {reserva['valor_estimado']}
kWh Consumido: {reserva['kwh_consumido']}

==========================================
""")
    return dict(reserva)

def editar_reserva(id_reserva, alteracao):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva = cursor.fetchone()

    if not reserva:
        print("Reserva nao encontrada.")
        conn.close()
        return None

    if alteracao == "status":
        nova_info = input("Digite o novo status (Agendada/Concluida/Cancelada): ")
        campo = "status_reserva"
        
    elif alteracao == "agendamento":
        nova_info_input = input("Digite a nova data (AAAA-MM-DD HH:MM): ")
        try:
            nova_info = datetime.strptime(nova_info_input.strip(), "%Y-%m-%d %H:%M").isoformat()
        except ValueError:
            print("Formato invalido.")
            conn.close()
            return None
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
        conn.close()
        return None

    if reserva[campo] == nova_info:
        print("Escolha um valor diferente.")
        conn.close()
        return None

    cursor.execute(f"UPDATE reservas SET {campo} = ? WHERE id_reserva = ?", (nova_info, id_reserva))
    conn.commit()
    
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva_atualizada = dict(cursor.fetchone())
    conn.close()
    
    print("Reserva updated com sucesso!")
    return reserva_atualizada

def deletar_reserva(id_reserva):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva = cursor.fetchone()

    if not reserva:
        print("Reserva nao encontrada.")
        conn.close()
        return None

    cursor.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva,))
    conn.commit()
    conn.close()
    
    print(f"Reserva {id_reserva} deletada com sucesso!")
    return dict(reserva)

def buscar_reserva_ativa_por_carregador(id_carregador):
    conn = conectar()
    cursor = conn.cursor()
    agora = datetime.now().isoformat()

    cursor.execute("""
        SELECT * FROM reservas 
        WHERE id_carregador = ? 
          AND status_reserva = ? 
          AND datetime(?) BETWEEN datetime(agendado_para) AND datetime(agendado_para, '+' || duracao_minutos || ' minutes')
    """, (id_carregador, STATUS_AGENDADA, agora))
    
    reserva = cursor.fetchone()
    conn.close()
    
    return dict(reserva) if reserva else None

def carregador_esta_reservado(id_carregador):
    return buscar_reserva_ativa_por_carregador(id_carregador) is not None

def obter_comando_estado_carregador(id_carregador):
    if carregador_esta_reservado(id_carregador):
        return f"RESERVED:{id_carregador}"
    return f"FREE:{id_carregador}"

def validar_liberacao_por_codigo(id_carregador, id_motorista, codigo_digitado, codigos_ativos):
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

    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE reservas SET status_reserva = ? WHERE id_reserva = ?",
        (STATUS_EM_ANDAMENTO, reserva["id_reserva"])
    )
    conn.commit()
    conn.close()

    return True, "Reserva validada. Uso permitido."