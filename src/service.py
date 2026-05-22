# service.py - Responsável por fornecer as funções de serviço para o sistema, como login, cadastro, controle de unidades e dispositivos.

# Responsavel por gerenciar os carregadores (CRUD)
import json
import random
from datetime import datetime
from database_manager import carregar_database, atualizar_database

dados = carregar_database()

# Definição dos tipos de entidades e seus intervalos de prefixo para geração de IDs
TIPOS = {
    "carregador": (0, 30),
    "unidade": (31, 50),
    "usuario": (51, 70),
    "reserva": (71, 99)
}

# Função para gerar um ID único para cada tipo de entidade
def gerar_id(tipo):
    if tipo not in TIPOS:
        raise ValueError("Tipo inválido")

    inicio, fim = TIPOS[tipo]

    prefixo = random.randint(inicio, fim)

    horario = datetime.now().strftime("%H%M%S")

    return f"{prefixo:02}{horario}"

# Carregadores
carregadores = dados.get("carregadores", {})

# Função responsável por criar um novo carregador
def criar_carregador(carregadores, id_unidade):

    id_carregador = gerar_id("carregador")

    if id_carregador in carregadores:
        print("ID de carregador já existe. Escolha outro.")
        return

    # Recebe as informacoes para criar o carregador
    modelo = input("Digite o modelo do carregador: ")
    fabricante = input("Digite o fabricante do carregador: ")
    tipo_corrente = input("Digite o tipo de corrente (AC/DC): ")
    potencia_kw = float(input("Digite a potência em kW: "))
    tipo_conector = input("Digite o tipo de conector: ")
    preco_por_kwh = float(input("Digite o preço por kWh: "))
    status_atual = input("Digite o status do carregador (Disponivel/Indisponivel): ")
    ultima_manutencao = input("Digite a data da última manutenção (AAAA-MM-DD): ")
    permite_reserva = input("Permite reserva? (true/false): ").lower()
    fila_virtual = input("Possui fila virtual? (true/false): ").lower()
    plug_and_charge = input("Possui Plug and Charge? (true/false): ").lower()

    # Adiciona as informacoes no banco de dados
    dados["carregadores"].update({

        id_carregador: {
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

# Função responsável por exibir o carregador
def visualizar_carregador(id_carregador):
    carregador = carregadores.get(id_carregador)
    if carregador:
        print(f"Carregador: {carregador['modelo'][:20]} - {carregador['fabricante']}")
    else:
        print("Carregador não encontrado.")

# Função responsável por editar o carregador
def editar_carregador(id_carregador, alteracao):
    carregador = dados.get("carregadores", {}).get(id_carregador)
    if carregador:
        # Responsavel por alterar o modelo
        if alteracao == "modelo":
            nova_info = input("Digite o novo modelo: ")

            if nova_info == carregador.get("modelo"):
                print("Por favor, escolha um modelo diferente do atual.")
                return

            carregador["modelo"] = nova_info

        # Responsavel por alterar o fabricante
        if alteracao == "fabricante":
            nova_info = input("Digite o novo fabricante: ")

            if nova_info == carregador.get("fabricante"):
                print("Por favor, escolha um fabricante diferente do atual.")
                return

            carregador["fabricante"] = nova_info

        # Responsavel por alterar o tipo de corrente
        if alteracao == "tipo_corrente":
            nova_info = input("Digite o novo tipo de corrente: ")

            if nova_info == carregador.get("tipo_corrente"):
                print("Escolha um tipo de corrente diferente.")
                return

            carregador["tipo_corrente"] = nova_info

        # Responsavel por alterar a potencia
        if alteracao == "potencia_kw":
            nova_info = float(input("Digite a nova potência: "))

            if nova_info == carregador.get("potencia_kw"):
                print("Escolha uma potência diferente.")
                return

            carregador["potencia_kw"] = nova_info

        # Responsavel por alterar ol tipo de conector
        if alteracao == "tipo_conector":
            nova_info = input("Digite o novo tipo de conector: ")

            if nova_info == carregador.get("tipo_conector"):
                print("Escolha um conector diferente.")
                return

            carregador["tipo_conector"] = nova_info

        # Responsavel por alterar o preco 
        if alteracao == "preco_por_kwh":
            nova_info = float(input("Digite o novo preço por kWh: "))

            if nova_info == carregador.get("preco_por_kwh"):
                print("Escolha um preço diferente.")
                return

            carregador["preco_por_kwh"] = nova_info

        # Responsavel por informar o status
        if alteracao == "status_atual":
            nova_info = input("Digite o novo status: ")

            if nova_info == carregador.get("status_atual"):
                print("Escolha um status diferente.")
                return

            carregador["status_atual"] = nova_info

        # Responsavel por informar a ultima manutencao
        if alteracao == "ultima_manutencao":
            nova_info = input("Digite a nova data: ")

            if nova_info == carregador.get("ultima_manutencao"):
                print("Escolha uma data diferente.")
                return

            carregador["ultima_manutencao"] = nova_info

        # Responsavel pela reserva
        if alteracao == "permite_reserva":
            nova_info = input("Permite reserva (true/false): ").lower() == "true"

            if nova_info == carregador["recursos"].get("permite_reserva"):
                print("O valor já é o atual.")
                return

            carregador["recursos"]["permite_reserva"] = nova_info

        # Responsavel pela fila virtual
        if alteracao == "fila_virtual":
            nova_info = input("Fila virtual (true/false): ").lower() == "true"

            if nova_info == carregador["recursos"].get("fila_virtual"):
                print("O valor já é o atual.")
                return

            carregador["recursos"]["fila_virtual"] = nova_info

        # Responsavel pela a alteracao do plug and charge
        if alteracao == "plug_and_charge":
            nova_info = input("Plug and Charge (true/false): ").lower() == "true"

            if nova_info == carregador["recursos"].get("plug_and_charge"):
                print("O valor já é o atual.")
                return

            carregador["recursos"]["plug_and_charge"] = nova_info
    else:
        print("Carregador não encontrado.")

# Função resposável por deletar o carregador
def deletar_carregador(id_carregador):  
    carregador = dados.get("carregador", {}).get(id_carregador)
    if carregador :
        del dados["carregadores"][id_carregador]
        atualizar_database(dados)
        print(f"carregador {id_carregador} foi deletado!")
    else:
        print("carregador não encontrado.")

# Unidades
units = dados.get("unidades", {})

def buscar_cep_info(cep):
    # Simulação de busca de informações do CEP

    return {
        "endereco_formatado": f"Endereço formatado para CEP {cep}",
        "coordenadas": {
            "latitude": -23.561684,
            "longitude": -46.625378
        }
    }

def criar_unidade(id_dono):
    # Gerar um ID único para a nova unidade
    id_unidade = gerar_id("unidade")

    # Coleta o nome da unidade e valida se já existe
    nome_unidade = input("Digite o nome da unidade: ")
    if nome_unidade in [unit.get("nome_unidade") for unit in units.values()]:
        print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
        return
    
    # Coleta o CEP e valida se já existe
    cep = input("Digite o CEP da unidade: ")
    if cep in [unit.get("CEP") for unit in units.values()]:
        print("CEP já cadastrado para outra unidade. Por favor, verifique o CEP e tente novamente.")
        return
    
    # Coleta o horário de abertura e valida se é uma entrada válida
    abertura = input("Digite o horário de abertura: ")
    if not abertura:
        print("Horário de abertura é obrigatório. Por favor, tente novamente.")
        return
    fechamento = input("Digite o horário de fechamento: ")
    if not fechamento:
        print("Horário de fechamento é obrigatório. Por favor, tente novamente.")
        return
    
    # Coleta se a unidade funciona aos finais de semana e valida a entrada
    funciona_fds = input("Funciona aos finais de semana? (s/n): ").lower()
    if funciona_fds == 's':
        funciona_fds = True
    elif funciona_fds == 'n':        
        funciona_fds = False
    else:
        print("Entrada inválida para funcionamento aos finais de semana. Por favor, digite 's' para sim ou 'n' para não.")
        return

    units.update({
        id_unidade: {
            "id_unidade": id_unidade,
            "id_dono": id_dono,
            "nome_unidade": nome_unidade,
            "CEP": cep,
            "endereco_formatado": buscar_cep_info(cep)["endereco_formatado"],
            "coordenadas": buscar_cep_info(cep)["coordenadas"],
            "horario_funcionamento": {
                "abertura": abertura,
                "fechamento": fechamento,
                "funciona_fds": funciona_fds
            },
            "avaliacao_media": 0.0
        }
    })
    
    atualizar_database(dados)

# Função responsável por exibir o carregador
def visualizar_unidade(id_unidade):
    unit = units.get(id_unidade)
    if unit:
        print(f"Unidade: {unit['nome_unidade']}")
    else:
        print("Unidade não encontrada.")

# Função responsável por editar o carregador
def editar_unidade(id_unidade, alteração):
    unit = dados.get("unidades", {}).get(id_unidade)

    if unit:
        print(f"Editando unidade: {unit['nome_unidade']}")
        # Altera o nome da unidade
        if alteração == "nome_unidade":
            nova_info = input("Digite o novo nome da unidade: ")

            if nova_info in [unit.get("nome_unidade") for unit in units.values()]:
                print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
                return
            unit["nome_unidade"] = nova_info

        # Altera o CEP da unidade
        if alteração == "CEP":
            nova_info = input("Digite o novo CEP da unidade: ")

            if nova_info in [unit.get("CEP") for unit in units.values()]:
                print("CEP já cadastrado para outra unidade. Por favor, verifique o CEP e tente novamente.")
                return

        # Altera o horário de funcionamento da unidade
        if alteração == "horario_funcionamento":
            nova_info_abertura = input("Digite o novo horário de abertura: ")
            nova_info_fechamento = input("Digite o novo horário de fechamento: ")

            if nova_info_funciona_fds == 's':
                nova_info_funciona_fds = True
            elif nova_info_funciona_fds == 'n':        
                nova_info_funciona_fds = False
            else:
                print("Entrada inválida para funcionamento aos finais de semana. Por favor, digite 's' para sim ou 'n' para não.")
                return

            unit["horario_funcionamento"] = {
                "abertura": nova_info_abertura,
                "fechamento": nova_info_fechamento,
                "funciona_fds": nova_info_funciona_fds
            }
    else:
        print("Unidade não encontrada.")

# Função resposável por deletar o carregador
def deletar_unidade(id_unidade):
    unit = dados.get("unidades", {}).get(id_unidade)
    if unit:
        del dados["unidades"][id_unidade]
        atualizar_database(dados)
        print(f"Unidade {id_unidade} deletada com sucesso.")
    else:
        print("Unidade não encontrada.")

while True:
    print("\nMenu de Unidades:")
    print("1. Criar Unidade")
    print("2. Visualizar Unidade")
    print("3. Editar Unidade")
    print("4. Deletar Unidade")
    print("5. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        id_dono = input("Digite o ID do dono da unidade: ")
        criar_unidade(id_dono)
    elif escolha == "2":
        id_unidade = input("Digite o ID da unidade: ")
        visualizar_unidade(id_unidade)
    elif escolha == "3":
        id_unidade = input("Digite o ID da unidade: ")
        alteração = input("Digite o campo a ser editado: ")
        editar_unidade(id_unidade, alteração)
    elif escolha == "4":
        id_unidade = input("Digite o ID da unidade: ")
        deletar_unidade(id_unidade)
    elif escolha == "5":
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")