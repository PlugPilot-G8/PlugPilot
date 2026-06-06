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
        id_unidade = input("Digite o ID da unidade: ").strip()
        cursor.execute("SELECT id_unidade FROM unidades WHERE id_unidade = ?", (id_unidade,))
        if not cursor.fetchone():
            print("Unidade nao encontrada.")
            conn.close()
            return None

        id_carregador = input("Digite o ID do carregador: ").strip()
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

    if carregador["status_atual"].upper() != "FREE":
        print("Carregador indisponivel.")
        conn.close()
        return None

    data_reserva = input("Digite a DATA da reserva (AAAA-MM-DD): ").strip()
    try:
        data_obj = datetime.strptime(data_reserva, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de data invalido. Use AAAA-MM-DD")
        conn.close()
        return None

    if data_obj < date.today():
        print("Nao e possivel agendar para uma data anterior ao dia atual.")
        conn.close()
        return None

    hora_reserva = input("Digite o HORARIO da reserva (HH:MM): ").strip()
    try:
        hora_obj = datetime.strptime(hora_reserva, "%H:%M").time()
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
    data_iso = data_obj.isoformat()
    hora_str = hora_obj.strftime("%H:%M")

    print("""
========= TEMPO DE RESERVA =========
  [1] 15 minutos  - R$  12,50
  [2] 30 minutes  - R$  25,00
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

def listar_reservas(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE id_motorista = ?", (id_usuario,))
    reservas = cursor.fetchall()
    
    if not reservas:
        print("Nenhuma reserva encontrada.")
        conn.close()
        return []

    lista_formatada = []
    for r in reservas:
        unidade = cursor.execute("SELECT nome_unidade FROM unidades WHERE id_unidade = ?", (r["id_unidade"],)).fetchone()
        carregador = cursor.execute("SELECT modelo FROM carregadores WHERE id_carregador = ?", (r["id_carregador"],)).fetchone()
        
        nome_unidade = unidade['nome_unidade'] if unidade else r["id_unidade"]
        modelo_carregador = carregador['modelo'] if carregador else r["id_carregador"]

        print(f"""
============================================
ID Reserva: {r['id_reserva']}
Unidade: {nome_unidade}
Carregador: {modelo_carregador}
Data: {r['data_reserva']}
Hora: {r['hora_reserva']}
Status: {r['status_reserva']}
Valor Estimado: R$ {r['valor_estimado']:.2f}
""")
        lista_formatada.append(dict(r))
        
    conn.close()
    return lista_formatada

def visualizar_reserva(id_reserva, id_motorista, serial_service=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva = cursor.fetchone()
    
    unidade = cursor.execute("SELECT nome_unidade FROM unidades WHERE id_unidade = ?", (reserva["id_unidade"],)).fetchone()
    carregador = cursor.execute("SELECT modelo FROM carregadores WHERE id_carregador = ?", (reserva["id_carregador"],)).fetchone()
    usuario = cursor.execute("SELECT nome FROM usuarios WHERE id_usuario = ?", (reserva["id_motorista"],)).fetchone()
        
    nome_unidade = unidade['nome_unidade'] if unidade else reserva["id_unidade"]
    modelo_carregador = carregador['modelo'] if carregador else reserva["id_carregador"]
    nome_usuario = usuario['nome'] if usuario else reserva["id_motorista"]
    
    conn.close()

    if not reserva:
        print("Reserva nao encontrada.")
        return None

    print(f"""
================ RESERVA =================

ID Reserva: {reserva['id_reserva']}
Motorista: {nome_usuario}
Unidade: {nome_unidade}
Carregador: {modelo_carregador}
Status: {reserva['status_reserva']}
Data: {reserva['data_reserva']}
Hora: {reserva['hora_reserva']}
Duracao: {reserva['duracao_minutos']} minutos
Valor Estimado: R$ {reserva['valor_estimado']:.2f}
kWh Consumido: {reserva['kwh_consumido']}

==========================================
""")
    
    mapeamento_edicao = {
        "1": "agendamento",
        "2": "duracao",
        "3": "valor",
        "4": "consumo"
    }

    while True:
        print("Gerenciar Reserva:")
        print("1. Editar Reserva")
        print("2. Deletar Reserva")
        print("3. Iniciar Recarga")
        print("4. Finalizar Reserva")
        print("5. Voltar")
        print("===========================================")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            while True:
                print("\nO que deseja editar?")
                print("1. Data/Hora da Reserva")
                print("2. Duracao da Reserva")
                print("3. Valor Estimado")
                print("4. kWh Consumido")
                print("5. Voltar")

                alteracao = input("Escolha uma opção: ").strip()

                if alteracao == "5":
                    break
                elif alteracao in mapeamento_edicao:
                    editar_reserva(id_reserva, mapeamento_edicao[alteracao])
                    break
                else:
                    print("Opção inválida.")
                
        elif opcao == "2":
            confirmacao = input("Tem certeza que deseja deletar esta reserva? (s/n): ").strip().lower()
            if confirmacao == "s":
                if deletar_reserva(id_reserva):
                    return None

        elif opcao == "3":
            if not serial_service:
                print("[SERIAL] Servico serial indisponivel.")
                continue

            codigo = input("Digite o codigo exibido no LCD: ").strip()
            sucesso = serial_service.liberar_por_codigo(
                id_carregador=reserva["id_carregador"],
                id_motorista=id_motorista,
                codigo_digitado=codigo,
                validar_liberacao_callback=validar_liberacao_por_codigo
            )

            if sucesso:
                print("[PlugPilot] Carregador liberado.")
                return None
            else:
                print("[PlugPilot] Codigo incorreto, expirado ou reserva invalida.")
                
        elif opcao == "4":
            if finalizar_reserva(id_reserva):
                return None

        elif opcao == "5":
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

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

    if alteracao == "agendamento":
        nova_data = input("Digite a nova DATA (AAAA-MM-DD): ").strip()
        try:
            data_obj = datetime.strptime(nova_data, "%Y-%m-%d").date()
        except ValueError:
            print("Formato de data invalido.")
            conn.close()
            return None

        if data_obj < date.today():
            print("Nao e possivel agendar para uma data anterior ao dia atual.")
            conn.close()
            return None

        nova_hora = input("Digite o novo HORARIO (HH:MM): ").strip()
        try:
            hora_obj = datetime.strptime(nova_hora, "%H:%M").time()
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
========= TEMPO DE RESERVA =========
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

        cursor.execute(
            "UPDATE reservas SET duracao_minutos = ?, valor_estimado = ? WHERE id_reserva = ?",
            (nova_info, novo_valor, id_reserva)
        )
        conn.commit()
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
        reserva_atualizada = dict(cursor.fetchone())
        conn.close()
        print("Reserva updated com sucesso!")
        return reserva_atualizada

    elif alteracao == "valor":
        nova_info = float(input("Digite o novo valor estimado: ").strip())
        campo = "valor_estimado"
        
    elif alteracao == "consumo":
        nova_info = float(input("Digite o consumo em kWh: ").strip())
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

def finalizar_reserva(id_reserva):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
    reserva = cursor.fetchone()

    if not reserva:
        print("Reserva nao encontrada.")
        conn.close()
        return False

    if reserva["status_reserva"] == STATUS_CONCLUIDA:
        print("Esta reserva ja foi finalizada anteriormente.")
        conn.close()
        return False

    cursor.execute(
        "UPDATE reservas SET status_reserva = ? WHERE id_reserva = ?",
        (STATUS_CONCLUIDA, id_reserva)
    )
    conn.commit()
    conn.close()
    
    print(f"Reserva {id_reserva} finalizada com sucesso!")
    return True

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

def obter_comando_estado_carregador(id_carregador):
    if buscar_reserva_ativa_por_carregador(id_carregador) is not None:
        return f"RESERVED:{id_carregador}"
    return f"FREE:{id_carregador}"

def validar_liberacao_por_codigo(id_carregador, id_motorista, codigo_digitado, codigos_ativos):
    reserva = buscar_reserva_ativa_por_carregador(id_carregador)

    if not reserva:
        return True, "Carregador livre. Uso permitido."

    if reserva["id_motorista"] != id_motorista:
        return False, "Este carregador esta reservado para outro usuario."

    id_normalizado = id_carregador.strip()
    codigo_info = codigos_ativos.get(id_normalizado)
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