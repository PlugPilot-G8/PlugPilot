# charger_manager.py - Gerenciamento dos carregadores.

from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id


STATUS_ARDUINO_PARA_SISTEMA = {
    "FREE": "Disponivel",
    "RESERVED": "Reservado",
    "IN_USE": "Ocupado",
    "LOCKED": "Reservado",
}


def _carregar():
    return carregar_database()


def _salvar(dados):
    atualizar_database(dados)


def buscar_id(nome_carregador, id_unidade):
    dados = _carregar()

    for id_carregador, carregador in dados.get("carregadores", {}).items():
        if (
            carregador.get("modelo") == nome_carregador
            and carregador.get("id_unidade") == id_unidade
        ):
            return id_carregador

    return None


def buscar_carregador_por_identificador(dados, identificador):
    carregadores = dados.get("carregadores", {})

    if identificador in carregadores:
        return identificador, carregadores[identificador]

    for id_carregador, carregador in carregadores.items():
        if carregador.get("id_hardware") == identificador:
            return id_carregador, carregador

    return None, None


def cadastrar_carregador(id_unidade):
    dados = _carregar()
    carregadores = dados.setdefault("carregadores", {})
    id_carregador = gerar_id("carregador")

    if id_carregador in carregadores:
        print("ID de carregador ja existe. Tente novamente.")
        return None

    modelo = input("Digite o modelo do carregador: ")
    fabricante = input("Digite o fabricante do carregador: ")
    tipo_corrente = input("Digite o tipo de corrente (AC/DC): ")
    potencia_kw = float(input("Digite a potencia em kW: "))
    tipo_conector = input("Digite o tipo de conector: ")
    preco_por_kwh = float(input("Digite o preco por kWh: "))
    status_atual = input("Digite o status do carregador (Disponivel/Indisponivel): ")
    ultima_manutencao = input("Digite a data da ultima manutencao (AAAA-MM-DD): ")
    id_hardware = input("Digite o ID do hardware Arduino (opcional): ").strip() or None

    permite_reserva = input("Permite reserva? (true/false): ").lower() == "true"
    fila_virtual = input("Possui fila virtual? (true/false): ").lower() == "true"
    plug_and_charge = input("Possui Plug and Charge? (true/false): ").lower() == "true"

    carregadores[id_carregador] = {
        "id_carregador": id_carregador,
        "id_unidade": id_unidade,
        "modelo": modelo,
        "fabricante": fabricante,
        "tipo_corrente": tipo_corrente,
        "potencia_kw": potencia_kw,
        "tipo_conector": tipo_conector,
        "preco_por_kwh": preco_por_kwh,
        "status_atual": status_atual,
        "tipo_monitoramento": "hardware" if id_hardware else "manual",
        "id_hardware": id_hardware,
        "ultima_manutencao": ultima_manutencao,
        "recursos": {
            "permite_reserva": permite_reserva,
            "fila_virtual": fila_virtual,
            "plug_and_charge": plug_and_charge,
        },
    }

    _salvar(dados)
    print(f"Carregador {id_carregador} criado com sucesso.")
    return carregadores[id_carregador]


def visualizar_carregador(id_usuario, id_carregador, serial_service=None):
    from ..managers.reserve_manager import reservar_carregador

    dados = _carregar()
    carregador = dados.get("carregadores", {}).get(id_carregador)
    usuario = dados.get("usuarios", {}).get(id_usuario)

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
                carregador = _carregar().get("carregadores", {}).get(id_carregador)
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
                    atualizar_status_carregador(id_carregador, "Reservado")
                    serial_service.enviar_comando(f"RESERVED:{id_carregador}")

                return
            elif opcao == "2":
                return
            else:
                print("Opcao invalida.")


def _menu_editar_carregador(id_carregador):
    opcoes = {
        "1": "modelo",
        "2": "fabricante",
        "3": "tipo_corrente",
        "4": "potencia_kw",
        "5": "tipo_conector",
        "6": "preco_por_kwh",
        "7": "status_atual",
        "8": "ultima_manutencao",
    }

    print("------ Editar Carregador ------")
    print("1. Modelo")
    print("2. Fabricante")
    print("3. Tipo de Corrente")
    print("4. Potencia (kW)")
    print("5. Tipo de Conector")
    print("6. Preco por kWh")
    print("7. Status Atual")
    print("8. Ultima Manutencao")
    print("9. Voltar")

    opcao = input("Escolha uma opcao: ")

    if opcao in opcoes:
        editar_carregador(id_carregador, opcoes[opcao])


def visualizar_carregadores(id_unidade):
    dados = _carregar()
    carregadores = [
        carregador
        for carregador in dados.get("carregadores", {}).values()
        if carregador.get("id_unidade") == id_unidade
    ]

    if not carregadores:
        print("Nenhum carregador cadastrado para esta unidade.")
        return

    for indice, carregador in enumerate(carregadores, start=1):
        print(
            f"{indice}. {carregador['modelo']} - {carregador['fabricante']} "
            f"(Status: {carregador['status_atual']})"
        )


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
            visualizar_carregador(id_usuario, id_carregador)
        elif opcao == "3":
            return
        else:
            print("Opcao invalida.")


def editar_carregador(id_carregador, alteracao):
    dados = _carregar()
    carregador = dados.get("carregadores", {}).get(id_carregador)

    if not carregador:
        print("Carregador nao encontrado.")
        return

    nova_info = input("Digite o novo valor: ")

    if alteracao in {"potencia_kw", "preco_por_kwh"}:
        nova_info = float(nova_info)

    if carregador.get(alteracao) == nova_info:
        print("Escolha um valor diferente do atual.")
        return

    carregador[alteracao] = nova_info
    _salvar(dados)
    print("Carregador atualizado com sucesso.")


def deletar_carregador(id_carregador):
    dados = _carregar()
    carregadores = dados.get("carregadores", {})

    if id_carregador not in carregadores:
        print("Carregador nao encontrado.")
        return

    del carregadores[id_carregador]
    _salvar(dados)
    print(f"Carregador {id_carregador} foi deletado!")


def atualizar_status_carregador(id_carregador, status_sistema):
    dados = _carregar()
    carregador = dados.get("carregadores", {}).get(id_carregador)

    if not carregador:
        print(f"[CHARGER_MANAGER] Carregador nao encontrado: {id_carregador}")
        return False

    carregador["status_atual"] = status_sistema
    _salvar(dados)
    print(f"[CHARGER_MANAGER] {id_carregador} -> {status_sistema}")
    return True


def atualizar_status_por_hardware(identificador, status_arduino):
    status_sistema = STATUS_ARDUINO_PARA_SISTEMA.get(status_arduino)

    if status_sistema is None:
        print(f"[CHARGER_MANAGER] Status invalido: {status_arduino}")
        return False

    dados = _carregar()
    id_carregador, carregador = buscar_carregador_por_identificador(dados, identificador)

    if not carregador:
        print(f"[CHARGER_MANAGER] Nenhum carregador vinculado a {identificador}")
        return False

    carregador["status_atual"] = status_sistema
    _salvar(dados)
    print(f"[CHARGER_MANAGER] {identificador} atualizou {id_carregador} para {status_sistema}")
    return True


def obter_vagas_unidade(id_unidade, dados):
    total_carregadores = 0
    carregadores_disponiveis = 0

    for carregador in dados.get("carregadores", {}).values():
        if carregador.get("id_unidade") == id_unidade:
            total_carregadores += 1
            if carregador.get("status_atual") == "Disponivel":
                carregadores_disponiveis += 1

    if total_carregadores == 0:
        return "(0/0)"

    return f"({carregadores_disponiveis}/{total_carregadores})"
