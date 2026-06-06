from datetime import datetime, date
from .database_manager import conectar
from ..services.service import gerar_id

STATUS_AGENDADA = "Agendada"
STATUS_EM_ANDAMENTO = "Em andamento"
STATUS_CONCLUIDA = "Concluida"

OPCOES_DURACAO = {
    "1": {"minutos": 15, "preco": 12.50},
    "2": {"minutos": 30, "preco": 25.00},
    "3": {"minutos": 45, "preco": 37.50},
    "4": {"minutos": 60, "preco": 50.00},
}

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


    data_reserva = input("Digite a DATA da reserva (AAAA-MM-DD): ")
    try:
        data_obj = datetime.strptime(data_reserva.strip(), "%Y-%m-%d").date()
    except ValueError:
        print("Formato de data invalido. Use AAAA-MM-DD")
        conn.close()
        return None

    if data_obj < date.today():
        print("Nao e possivel agendar para uma data anterior ao dia atual.")
        conn.close()
        return None

    hora_reserva = input("Digite o HORARIO da reserva (HH:MM): ")
    try:
        hora_obj = datetime.strptime(hora_reserva.strip(), "%H:%M").time()
    except ValueError:
        print("Formato de horario invalido. Use HH:MM")
        conn.close()
        return None

    data_hora_obj = datetime.combine(data_obj, hora_obj)

    if data_hora_obj < datetime.now():
        print("Nao e possivel agendar para um horario que ja passou.")
        conn.close()
        return None

    data_formatada = data_hora_obj.isoformat()
    data_iso = data_obj.isoformat()       # MODIFICADO: chave separada para data (linha 96)
    hora_str = hora_obj.strftime("%H:%M") # MODIFICADO: chave separada para hora (linha 97)

    
    print("""
========= TEMPO DE RECARGA =========
  [1] 15 minutos  - R$  12,50
  [2] 30 minutos  - R$  25,00
  [3] 45 minutos  - R$  37,50
  [4] 60 minutos  - R$  50,00
====================================
""")
    opcao = input("Escolha uma opcao (1-4): ").strip()
    if opcao not in OPCOES_DURACAO:
        print("Opcao invalida.")
        conn.close()
        return None

    duracao_minutos = OPCOES_DURACAO[opcao]["minutos"]
    valor_estimado = OPCOES_DURACAO[opcao]["preco"]

    id_reserva = gerar_id("reserva")


    cursor.execute("""
        INSERT INTO reservas (
            id_reserva, id_motorista, id_unidade, id_carregador, 
            status_reserva, agendado_para, data_reserva, hora_reserva,
            duracao_minutos, valor_estimado, kwh_consumido
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_reserva, id_motorista, id_unidade, id_carregador,
        STATUS_AGENDADA, data_formatada, data_iso, hora_str,
        duracao_minutos, valor_estimado, 0.0
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

    # MODIFICADO: exibe data e hora separadamente no print (linhas 148-149)
    print(f"""
================ RESERVA =================

ID Reserva: {reserva['id_reserva']}
Motorista: {reserva['id_motorista']}
Unidade: {reserva['id_unidade']}
Carregador: {reserva['id_carregador']}
Status: {reserva['status_reserva']}
Data: {reserva['data_reserva']}
Hora: {reserva['hora_reserva']}
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
        nova_data = input("Digite a nova DATA (AAAA-MM-DD): ")
        try:
            data_obj = datetime.strptime(nova_data.strip(), "%Y-%m-%d").date()
        except ValueError:
            print("Formato de data invalido.")
            conn.close()
            return None

        if data_obj < date.today():
            print("Nao e possivel agendar para uma data anterior ao dia atual.")
            conn.close()
            return None

        nova_hora = input("Digite o novo HORARIO (HH:MM): ")
        try:
            hora_obj = datetime.strptime(nova_hora.strip(), "%H:%M").time()
        except ValueError:
            print("Formato de horario invalido.")
            conn.close()
            return None

        data_hora_obj = datetime.combine(data_obj, hora_obj)
        if data_hora_obj < datetime.now():
            print("Nao e possivel agendar para um horario que ja passou.")
            conn.close()
            return None

        nova_info = data_hora_obj.isoformat()
        cursor.execute(
            "UPDATE reservas SET agendado_para = ?, data_reserva = ?, hora_reserva = ? WHERE id_reserva = ?",
            (nova_info, data_obj.isoformat(), hora_obj.strftime("%H:%M"), id_reserva)
        )
        conn.commit()
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
        reserva_atualizada = dict(cursor.fetchone())
        conn.close()
        print("Reserva atualizada com sucesso!")
        return reserva_atualizada

    elif alteracao == "duracao":
        print("""
========= TEMPO DE RECARGA =========
  [1] 15 minutos  - R$  12,50
  [2] 30 minutos  - R$  25,00
  [3] 45 minutos  - R$  37,50
  [4] 60 minutos  - R$  50,00
====================================
""")
        opcao = input("Escolha uma opcao (1-4): ").strip()
        if opcao not in OPCOES_DURACAO:
            print("Opcao invalida.")
            conn.close()
            return None
        nova_info = OPCOES_DURACAO[opcao]["minutos"]
        novo_valor = OPCOES_DURACAO[opcao]["preco"]
        campo = "duracao_minutos"

        cursor.execute(
            "UPDATE reservas SET duracao_minutos = ?, valor_estimado = ? WHERE id_reserva = ?",
            (nova_info, novo_valor, id_reserva)
        )
        conn.commit()
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
        reserva_atualizada = dict(cursor.fetchone())
        conn.close()
        print("Reserva atualizada com sucesso!")
        return reserva_atualizada

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
    
    print("Reserva atualizada com sucesso!")
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