# charger_manager.py - Gerenciamento dos carregadores via SQLite.

from .database_manager import conectar
from ..services.service import gerar_id
import sqlite3

STATUS_ARDUINO_PARA_SISTEMA = {
    "FREE": "FREE",
    "RESERVED": "RESERVED",
    "IN_USE": "IN_USE",
    "LOCKED": "RESERVED",
}

def buscar_id(nome_carregador, id_unidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_carregador FROM carregadores WHERE modelo = ? AND id_unidade = ?",
        (nome_carregador, id_unidade)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado["id_carregador"] if resultado else None

def buscar_carregador_por_identificador(identificador):
    conn = conectar()
    cursor = conn.cursor()

    identificador_normalizado = (
        identificador.strip()
        .upper()
        .replace("HARDWARE_", "")
        .replace("_", "")
    )

    cursor.execute(
        """
        SELECT * FROM carregadores
        WHERE UPPER(REPLACE(REPLACE(id_carregador, 'HARDWARE_', ''), '_', '')) = ?
           OR UPPER(REPLACE(REPLACE(id_hardware, 'HARDWARE_', ''), '_', '')) = ?
        """,
        (identificador_normalizado, identificador_normalizado)
    )
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return resultado["id_carregador"], resultado
    return None, None

def cadastrar_carregador(id_unidade):
    id_carregador = gerar_id("carregador")

    modelo = input("Digite o modelo do carregador: ")
    fabricante = input("Digite o fabricante do carregador: ")
    tipo_corrente = input("Digite o tipo de corrente (AC/DC): ")
    potencia_kw = float(input("Digite a potencia em kW: "))
    tipo_conector = input("Digite o tipo de conector: ")
    preco_por_kwh = float(input("Digite o preco por kWh: "))
    status_atual = "Disponivel"
    ultima_manutencao = input("Digite a data da ultima manutencao (AAAA-MM-DD): ")
    id_hardware = input("Digite o ID do hardware Arduino (opcional): ").strip() or None

    permite_reserva = 1 if input("Permite reserva? (true/false): ").lower() == "true" else 0
    fila_virtual = 1 if input("Possui fila virtual? (true/false): ").lower() == "true" else 0
    plug_and_charge = 1 if input("Possui Plug and Charge? (true/false): ").lower() == "true" else 0

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO carregadores (
                id_carregador, id_unidade, modelo, fabricante, tipo_corrente, 
                potencia_kw, tipo_conector, preco_por_kwh, status_atual, 
                tipo_monitoramento, id_hardware, ultima_manutencao, 
                permite_reserva, fila_virtual, plug_and_charge
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_carregador, id_unidade, modelo, fabricante, tipo_corrente,
            potencia_kw, tipo_conector, preco_por_kwh, status_atual,
            "hardware" if id_hardware else "manual", id_hardware, ultima_manutencao,
            permite_reserva, fila_virtual, plug_and_charge
        ))
        conn.commit()
        print(f"Carregador {id_carregador} criado com sucesso.")
        
        cursor.execute("SELECT * FROM carregadores WHERE id_carregador = ?", (id_carregador,))
        carregador_criado = cursor.fetchone()
        return carregador_criado
    except sqlite3.IntegrityError:
        print("Erro de integridade (ID de carregador ja existe ou unidade invalida).")
        return None
    finally:
        conn.close()

def visualizar_carregador(id_usuario, id_carregador, serial_service=None):
    from .reserve_manager import reservar_carregador

    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM carregadores WHERE id_carregador = ?", (id_carregador,))
    carregador = cursor.fetchone()
    
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    usuario = cursor.fetchone()
    conn.close()

    if not carregador:
        print("Carregador nao encontrado.")
        return

    if not usuario:
        print("Usuario nao encontrado.")
        return

    while True:
        print(f"\n------ Informacoes do {carregador['modelo']} ------")
        print(f"Modelo: {carregador['modelo']}")
        print(f"Fabricante: {carregador['fabricante']}")
        print(f"Tipo de Corrente: {carregador['tipo_corrente']}")
        print(f"Potencia (kW): {carregador['potencia_kw']}")
        print(f"Tipo de Conector: {carregador['tipo_conector']}")
        print(f"Preco por kWh: {carregador['preco_por_kwh']}")
        print(f"Status Atual: {carregador['status_atual']}")
        print(f"Ultima Manutencao: {carregador['ultima_manutencao']}")

        if usuario["tipo_usuario"] == "empresario":
            print("---------------------------------------------")
            print("1. Editar Carregador")
            print("2. Deletar Carregador")
            print("3. Voltar")
            opcao = input("Escolha uma opcao: ")

            if opcao == "1":
                _menu_editar_carregador(id_carregador)
                
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM carregadores WHERE id_carregador = ?", (id_carregador,))
                carregador = cursor.fetchone()
                conn.close()
            elif opcao == "2":
                deletar_carregador(id_carregador)
                return
            elif opcao == "3":
                return
            else:
                print("Opcao invalida.")

        elif usuario["tipo_usuario"] == "motorista":
            print("---------------------------------------------")
            print("1. Reservar Carregador")
            print("2. Voltar")
            opcao = input("Escolha uma opcao: ")

            if opcao == "1":
                reserva = reservar_carregador(id_usuario, id_carregador)

                if reserva and serial_service:
                    atualizar_status_carregador(id_carregador, "RESERVED")
                    serial_service.enviar_comando(f"RESERVED:{id_carregador}")
                return
            elif opcao == "2":
                return
            else:
                print("Opcao invalida.")

def _menu_editar_carregador(id_carregador):
    opcoes = {
        "1": "modelo", "2": "fabricante", "3": "tipo_corrente",
        "4": "potencia_kw", "5": "tipo_conector", "6": "preco_por_kwh",
        "7": "status_atual", "8": "ultima_manutencao",
    }

    print("------ Editar Carregador ------")
    print("1. Modelo") 
    print("2. Fabricante") 
    print("3. Tipo de Corrente")
    print("4. Potencia (kW)") 
    print("5. Tipo de Conector") 
    print("6. Preco por kWh")
    print("7. Status Atual"), 
    print("8. Ultima Manutencao"), 
    print("9. Voltar")

    opcao = input("Escolha uma opcao: ")
    if opcao in opcoes:
        editar_carregador(id_carregador, opcoes[opcao])

def visualizar_carregadores(id_unidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carregadores WHERE id_unidade = ?", (id_unidade,))
    carregadores = cursor.fetchall()
    conn.close()

    if not carregadores:
        print("Nenhum carregador cadastrado para esta unidade.")
        return

    for indice, carregador in enumerate(carregadores, start=1):
        print(f"{indice}. {carregador['modelo']} - {carregador['fabricante']} (Status: {carregador['status_atual']})")

def gerenciar_carregadores(id_usuario, id_unidade):
    while True:
        print("------ Carregadores da Unidade ------")
        visualizar_carregadores(id_unidade)
        print("------------------------------------")
        print("1. Cadastrar Carregador")
        print("2. Visualizar Carregador")
        print("3. Voltar")

        opcao = input("Escolha uma opcao: ")
        if opcao == "1":
            cadastrar_carregador(id_unidade)
        elif opcao == "2":
            nome_carregador = input("Digite o nome do carregador: ")
            id_carregador = buscar_id(nome_carregador, id_unidade)
            if id_carregador:
                visualizar_carregador(id_usuario, id_carregador)
            else:
                print("Carregador nao encontrado.")
        elif opcao == "3":
            return
        else:
            print("Opcao invalida.")

def editar_carregador(id_carregador, alteracao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carregadores WHERE id_carregador = ?", (id_carregador,))
    carregador = cursor.fetchone()

    if not carregador:
        print("Carregador nao encontrado.")
        conn.close()
        return

    nova_info = input("Digite o novo valor: ")
    if alteracao in {"potencia_kw", "preco_por_kwh"}:
        nova_info = float(nova_info)

    if carregador[alteracao] == nova_info:
        print("Escolha um valor diferente do atual.")
        conn.close()
        return

    cursor.execute(f"UPDATE carregadores SET {alteracao} = ? WHERE id_carregador = ?", (nova_info, id_carregador))
    conn.commit()
    conn.close()
    print("Carregador atualizado com sucesso.")

def deletar_carregador(id_carregador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carregadores WHERE id_carregador = ?", (id_carregador,))
    linhas_afetadas = cursor.rowcount
    conn.commit()
    conn.close()

    if linhas_afetadas == 0:
        print("Carregador nao encontrado.")
    else:
        print(f"Carregador {id_carregador} foi deletado!")

def atualizar_status_carregador(id_carregador, status_sistema):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE carregadores SET status_atual = ? WHERE id_carregador = ?", (status_sistema, id_carregador))
    linhas_afetadas = cursor.rowcount
    conn.commit()
    conn.close()

    if linhas_afetadas == 0:
        print(f"[CHARGER_MANAGER] Carregador nao encontrado: {id_carregador}")
        return False

    return True

def atualizar_status_por_hardware(identificador, status_arduino):
    status_sistema = STATUS_ARDUINO_PARA_SISTEMA.get(status_arduino)
    
    if status_sistema is None:
        print(f"[CHARGER_MANAGER] Status invalido: {status_arduino}")
        return False

    id_carregador, carregador = buscar_carregador_por_identificador(identificador)
    
    if not carregador:
        print(f"[CHARGER_MANAGER] Nenhum carregador vinculado a {identificador}")
        return False

    return atualizar_status_carregador(id_carregador, status_sistema)

def obter_vagas_unidade(id_unidade):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM carregadores WHERE id_unidade = ?", (id_unidade,))
    total_carregadores = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*) FROM carregadores
        WHERE id_unidade = ?
          AND UPPER(status_atual) IN ('FREE', 'DISPONIVEL')
        """,
        (id_unidade,)
    )
    carregadores_disponiveis = cursor.fetchone()[0]
    
    conn.close()

    if total_carregadores == 0:
        return "(0/0)"

    return f"({carregadores_disponiveis}/{total_carregadores})"
