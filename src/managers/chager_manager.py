# charger_manager.py - Gerenciamento e CRUD dos carregadores
from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id

salvar_database = atualizar_database

dados = carregar_database()

STATUS_ARDUINO_PARA_SISTEMA = {
    "IN_USE": "Ocupado",
    "FREE": "Disponivel"
}

def buscar_id(nome_carregador, id_unidade):
    carregadores = dados.get("carregadores", {})
    for id_carregador, carregador in carregadores.items():
        if carregador["modelo"] == nome_carregador and carregador["id_unidade"] == id_unidade:
            return id_carregador
    return None

# Função para criar um novo carregador
def cadastrar_carregador(id_unidade):
    carregadores = dados.get("carregadores", {})
    
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

def visualizar_carregador(id_usuario, id_carregador):
    from ..managers.reserve_manager import reservar_carregador
    
    carregador = dados.get("carregadores", {}).get(id_carregador)
    usuario = dados.get("usuarios", {}).get(id_usuario)

    if carregador:
        tipo_usuario = usuario.get("tipo_usuario")
        
        while True:
            print(f"\n------ Informações do {carregador['modelo']} ------")
            print(f"Modelo: {carregador['modelo']}")
            print(f"Fabricante: {carregador['fabricante']}")
            print(f"Tipo de Corrente: {carregador['tipo_corrente']}")
            print(f"Potência (kW): {carregador['potencia_kw']}")
            print(f"Tipo de Conector: {carregador['tipo_conector']}")
            print(f"Preço por kWh: {carregador['preco_por_kwh']}")
            print(f"Status Atual: {carregador['status_atual']}")
            print(f"Última Manutenção: {carregador['ultima_manutencao']}")
            print("Recursos:")
            if tipo_usuario == "empresario":
                for recurso, valor in carregador["recursos"].items():
                    print(f"  - {recurso}: {'Sim' if valor else 'Não'}")
                
            if usuario["tipo_usuario"] == "empresario":
                print("---------------------------------------------")
                print("1. Editar Carregador")
                print("2. Deletar Carregador")
                print("3. Voltar")
                opcao = input("Escolha uma opção: ")
                
                if opcao == "1":
                    while True:
                        print("------ Editar Carregador ------")
                        print("\nO que deseja alterar?")
                        print("1. Modelo")
                        print("2. Fabricante")
                        print("3. Tipo de Corrente")
                        print("4. Potência (kW)")
                        print("5. Tipo de Conector")
                        print("6. Preço por kWh")
                        print("7. Status Atual")
                        print("8. Última Manutenção")
                        print("9. Voltar")
                        print("--------------------------------")
                        opcao_alteracao = input("Escolha uma opção: ")
                        if opcao_alteracao == "1":
                            editar_carregador(id_carregador, "modelo")
                            break
                        elif opcao_alteracao == "2":
                            editar_carregador(id_carregador, "fabricante")
                            break
                        elif opcao_alteracao == "3":
                            editar_carregador(id_carregador, "tipo_corrente")
                            break
                        elif opcao_alteracao == "4":
                            editar_carregador(id_carregador, "potencia_kw")
                            break
                        elif opcao_alteracao == "5":
                            editar_carregador(id_carregador, "tipo_conector")
                            break
                        elif opcao_alteracao == "6":
                            editar_carregador(id_carregador, "preco_por_kwh")
                            break
                        elif opcao_alteracao == "7":
                            editar_carregador(id_carregador, "status_atual")
                            break
                        elif opcao_alteracao == "8":
                            editar_carregador(id_carregador, "ultima_manutencao")
                            break
                        elif opcao_alteracao == "9":
                            break
                        else:
                            print("Opção inválida. Por favor, tente novamente.")
                elif opcao == "2":
                    deletar_carregador(id_carregador)
                    return
                elif opcao == "3":
                    break
            elif usuario["tipo_usuario"] == "motorista":
                print("---------------------------------------------")
                print("1. Reservar Carregador")
                print("2. Voltar")
                print("---------------------------------------------")
                
                opcao = input("Escolha uma opção: ")
                
                if opcao == "1":
                    reservar_carregador(id_usuario, id_carregador)
                    break
                elif opcao == "2":
                    break
            
    else:
        print("Carregador não encontrado.")

def visualizar_carregadores(id_unidade):
    carregadores = dados.get("carregadores", {})
    carregadores_unidade = [carregador for carregador in carregadores.values() if carregador["id_unidade"] == id_unidade]

    if carregadores_unidade:
        for i, carregador in enumerate(carregadores_unidade, start=1):
            print(f"{i}. {carregador['modelo']} - {carregador['fabricante']} (Status: {carregador['status_atual']})")
    else:
        print("Nenhum carregador cadastrado para esta unidade.")

def gerenciar_carregadores(id_usuario, id_unidade):
    while True:
        print("------ Carregadores da Unidade ------")
        carregadores = dados.get("carregadores", {})
        carregadores_unidade = [carregador for carregador in carregadores.values() if carregador["id_unidade"] == id_unidade]

        if carregadores_unidade:
            for i, carregador in enumerate(carregadores_unidade, start=1):
                print(f"{i}. {carregador['modelo']} - {carregador['fabricante']}")
        else:
            print("Nenhum carregador cadastrado para esta unidade.")
            
        print("------------------------------------")
        print("1. Cadastrar Carregador")
        print("2. Visualizar Carregador")
        print("------------------------------------")
        print("3. Voltar")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_carregador(id_unidade)
            
        elif opcao == "2":
            nome_carregador = input("Digite o nome do carregador: ")
            id_carregador = buscar_id(nome_carregador, id_unidade)
            visualizar_carregador(id_usuario, id_carregador)
            
        elif opcao == "3":
            break
        
        else:
            print("Opção inválida. Por favor, tente novamente.")

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

# Função para deletar um carregador do sistema
def deletar_carregador(id_carregador):
    carregador = dados.get("carregadores", {}).get(id_carregador)

    if carregador:
        del dados["carregadores"][id_carregador]
        atualizar_database(dados)
        print(f"Carregador {id_carregador} foi deletado!")
    else:
        print("Carregador não encontrado.")

# Função para atualizar o status do carregador
def atualizar_status_por_hardware(id_hardware, status_arduino):
    dados = carregar_database()

    novo_status = STATUS_ARDUINO_PARA_SISTEMA.get(status_arduino)

    if novo_status is None:
        print(f"[CHARGER_MANAGER] Status inválido: {status_arduino}")
        return False

    for id_carregador, carregador in dados.get("carregadores", {}).items():
        if carregador.get("id_hardware") == id_hardware:
            carregador["status_atual"] = novo_status
            salvar_database(dados)

            print(
                f"[CHARGER_MANAGER] Hardware {id_hardware} atualizou "
                f"{id_carregador} para {novo_status}"
            )

            return True

    print(f"[CHARGER_MANAGER] Nenhum carregador vinculado ao hardware {id_hardware}")
    return False

def obter_vagas_unidade(id_unidade, dados):
    carregadores = dados.get("carregadores", {})
    total_carregadores = 0
    carregadores_disponiveis = 0
    
    for carregador in carregadores.values():
        if carregador.get("id_unidade") == id_unidade:
            total_carregadores += 1
            if carregador.get("status_atual") == "Disponivel":
                carregadores_disponiveis += 1
                
    if total_carregadores == 0:
        return "(0/0)"
    return f"({carregadores_disponiveis}/{total_carregadores})"