# charger_manager.py - Gerenciamento e CRUD dos carregadores
from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id

dados = carregar_database()

# Carregadores
carregadores = dados.get("carregadores", {})

# Função para criar um novo carregador
def criar_carregador(carregadores, id_unidade):
    id_carregador = gerar_id("carregador")

    if id_carregador in carregadores:
        print("ID de carregador já existe. Tente novamente.")
        return

    # Recebe as informações do carregador
    modelo = input("Digite o modelo do carregador: ")
    fabricante = input("Digite o fabricante do carregador: ")
    tipo_corrente = input("Digite o tipo de corrente (AC/DC): ")
    potencia_kw = float(input("Digite a potência em kW: "))
    tipo_conector = input("Digite o tipo de conector: ")
    preco_por_kwh = float(input("Digite o preço por kWh: "))
    status_atual = input("Digite o status do carregador (Disponivel/Indisponivel): ")
    ultima_manutencao = input("Digite a data da última manutenção (AAAA-MM-DD): ")

    permite_reserva = input("Permite reserva? (true/false): ").lower() == "true"
    fila_virtual = input("Possui fila virtual? (true/false): ").lower() == "true"
    plug_and_charge = input("Possui Plug and Charge? (true/false): ").lower() == "true"

    # Atualiza as informações do carregador no banco de dados
    dados["carregadores"].update({
        id_carregador: {
            "id_carregador": id_carregador,
            "id_unidade": id_unidade,
            "modelo": modelo,
            "fabricante": fabricante,
            "tipo_corrente": tipo_corrente,
            "potencia_kw": potencia_kw,
            "tipo_conector": tipo_conector,
            "preco_por_kwh": preco_por_kwh,
            "status_atual": status_atual,
            "ultima_manutencao": ultima_manutencao,
            "recursos": {
                "permite_reserva": permite_reserva,
                "fila_virtual": fila_virtual,
                "plug_and_charge": plug_and_charge
            }
        }
    })

    atualizar_database(dados)
    print(f"Carregador {id_carregador} criado com sucesso.")

# Função para visualizar as informações de um carregador específico
def visualizar_carregador(id_carregador):
    carregador = dados.get("carregadores", {}).get(id_carregador)

    if carregador:
        print(f"Carregador: {carregador['modelo'][:20]} - {carregador['fabricante']}")
    else:
        print("Carregador não encontrado.")

# Função para editar as informações de um carregador existente
def editar_carregador(id_carregador, alteracao):
    carregador = dados.get("carregadores", {}).get(id_carregador)

    # Verifica se o carregador existe no banco de dados antes de realizar as alterações
    if carregador:
        # Recebe a nova informação a ser atualizada e valida de acordo com o tipo de alteração, garantindo que a nova informação seja diferente da atual
        if alteracao == "modelo":
            nova_info = input("Digite o novo modelo: ")

            if nova_info == carregador.get("modelo"):
                print("Por favor, escolha um modelo diferente do atual.")
                return

            carregador["modelo"] = nova_info

        if alteracao == "fabricante":
            nova_info = input("Digite o novo fabricante: ")

            if nova_info == carregador.get("fabricante"):
                print("Por favor, escolha um fabricante diferente do atual.")
                return

            carregador["fabricante"] = nova_info

        if alteracao == "tipo_corrente":
            nova_info = input("Digite o novo tipo de corrente: ")

            if nova_info == carregador.get("tipo_corrente"):
                print("Escolha um tipo de corrente diferente.")
                return

            carregador["tipo_corrente"] = nova_info

        if alteracao == "potencia_kw":
            nova_info = float(input("Digite a nova potência: "))

            if nova_info == carregador.get("potencia_kw"):
                print("Escolha uma potência diferente.")
                return

            carregador["potencia_kw"] = nova_info

        if alteracao == "tipo_conector":
            nova_info = input("Digite o novo tipo de conector: ")

            if nova_info == carregador.get("tipo_conector"):
                print("Escolha um conector diferente.")
                return

            carregador["tipo_conector"] = nova_info

        if alteracao == "preco_por_kwh":
            nova_info = float(input("Digite o novo preço por kWh: "))

            if nova_info == carregador.get("preco_por_kwh"):
                print("Escolha um preço diferente.")
                return

            carregador["preco_por_kwh"] = nova_info

        if alteracao == "status_atual":
            nova_info = input("Digite o novo status: ")

            if nova_info == carregador.get("status_atual"):
                print("Escolha um status diferente.")
                return

            carregador["status_atual"] = nova_info

        if alteracao == "ultima_manutencao":
            nova_info = input("Digite a nova data: ")

            if nova_info == carregador.get("ultima_manutencao"):
                print("Escolha uma data diferente.")
                return

            carregador["ultima_manutencao"] = nova_info

        if alteracao == "permite_reserva":
            nova_info = input("Permite reserva (true/false): ").lower() == "true"

            if nova_info == carregador["recursos"].get("permite_reserva"):
                print("O valor já é o atual.")
                return

            carregador["recursos"]["permite_reserva"] = nova_info

        if alteracao == "fila_virtual":
            nova_info = input("Fila virtual (true/false): ").lower() == "true"

            if nova_info == carregador["recursos"].get("fila_virtual"):
                print("O valor já é o atual.")
                return

            carregador["recursos"]["fila_virtual"] = nova_info

        if alteracao == "plug_and_charge":
            nova_info = input("Plug and Charge (true/false): ").lower() == "true"

            if nova_info == carregador["recursos"].get("plug_and_charge"):
                print("O valor já é o atual.")
                return

            carregador["recursos"]["plug_and_charge"] = nova_info

        # Atualiza as informações do carregador no banco de dados
        atualizar_database(dados)
        print("Carregador atualizado com sucesso.")
    else:
        print("Carregador não encontrado.")

# Função para deletar um carregador do sistema, verificando se o ID do carregador existe no banco de dados antes de realizar a exclusão
def deletar_carregador(id_carregador):
    carregador = dados.get("carregadores", {}).get(id_carregador)

    if carregador:
        del dados["carregadores"][id_carregador]
        atualizar_database(dados)
        print(f"Carregador {id_carregador} foi deletado!")
    else:
        print("Carregador não encontrado.")