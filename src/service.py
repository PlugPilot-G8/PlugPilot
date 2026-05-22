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

# Função para buscar informações do CEP (simulação)
def buscar_cep_info(cep):
    # Simulação de busca de informações do CEP

    return {
        "endereco_formatado": f"Endereço formatado para CEP {cep}",
        "coordenadas": {
            "latitude": -23.561684,
            "longitude": -46.625378
        }
    }

# Carregadores
chargers = dados.get("carregadores", {})

# Função responsável por criar um novo carregador
def criar_carregador(chargers,  id_unidade):
    id_carregador = gerar_id("carregador")
    if id_carregador in chargers:
        print("ID de carregador já existe. Por favor, escolha um ID diferente.")
        return
    
    modelo = input("Digite o modelo do carregador: ")
    fabricante = input("Digite o fabricante do carregador: ")
    tipo_corrente = input("Digite o tipo de corrente (AC/DC): ")
    potencia_kw = float(input("Digite a potência em kW: "))
    tipo_conector = input("Digite o tipo de conector: ")
    preco_por_kwh = float(input("Digite o preço por kWh: "))
    
    dados["carregadores"].update({
        id_carregador: {
            "id_unidade": id_unidade,
            "modelo": modelo,
            "fabricante": fabricante,
            "tipo_corrente": tipo_corrente,
            "potencia_kw": potencia_kw,
            "tipo_conector": tipo_conector,
            "preco_por_kwh": preco_por_kwh
        }
    })
    
    atualizar_database(dados)

# Função responsável por exibir o carregador
def visualizar_carregador(id_carregador):
    charger = chargers.get(id_carregador)
    if charger:
        print(f"Carregador: {charger['modelo'][:20]} - {charger['fabricante']}")
    else:
        print("Carregador não encontrado.")

# Função responsável por editar o carregador
def editar_carregador():
    print("editando carregador...")

# Função resposável por deletar o carregador
def deletar_carregador():
    print("deletando carregador...")

# Unidades
unidades = dados.get("unidades", {})

# Função responsável por criar uma nova unidade
def criar_unidade(id_dono):
    # Gerar um ID único para a nova unidade
    id_unidade = gerar_id("unidade")

    # Coleta o nome da unidade e valida se já existe
    nome_unidade = input("Digite o nome da unidade: ")
    if nome_unidade in [unidade.get("nome_unidade") for unidade in unidades.values()]:
        print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
        return
    
    # Coleta o CEP e valida se já existe
    cep = input("Digite o CEP da unidade: ")
    if cep in [unidade.get("CEP") for unidade in unidades.values()]:
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

    unidades.update({
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
    unidade = unidades.get(id_unidade)
    if unidade:
        print(f"-------------------- {unidade['nome_unidade']} --------------------")
        print(f"Endereço: {unidade['endereco_formatado']}")
        print(f"Horário de Funcionamento: {unidade['horario_funcionamento']['abertura']} - {unidade['horario_funcionamento']['fechamento']}")
        print(f"Funciona aos Finais de Semana: {'Sim' if unidade['horario_funcionamento']['funciona_fds'] else 'Não'}")
        print(f"Avaliação Média: {unidade['avaliacao_media']}")

        print("\nCarregadores:")
        for i in chargers.values():
            if i["id_unidade"] == id_unidade:
                visualizar_carregador(i["id_carregador"])
        print(f"--------------------------------------------------------------------")
    else:
        print("Unidade não encontrada.")

visualizar_unidade("und_001")

# Função responsável por editar o carregador
def editar_unidade(id_unidade, alteracao):
    unidade = dados.get("unidades", {}).get(id_unidade)

    if unidade:
        print(f"Editando unidade: {unidade['nome_unidade']}")
        # Altera o nome da unidade
        if alteracao == "nome_unidade":
            nova_info = input("Digite o novo nome da unidade: ")

            if nova_info in [unidade.get("nome_unidade") for unidade in unidades.values()]:
                print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
                return
            unidade["nome_unidade"] = nova_info

        # Altera o CEP da unidade
        if alteracao == "CEP":
            nova_info = input("Digite o novo CEP da unidade: ")

            if nova_info in [unidade.get("CEP") for unidade in unidades.values()]:
                print("CEP já cadastrado para outra unidade. Por favor, verifique o CEP e tente novamente.")
                return
            unidade["CEP"] = nova_info

        # Altera o horário de funcionamento da unidade
        if alteracao == "horario_funcionamento":
            nova_info_abertura = input("Digite o novo horário de abertura: ")
            nova_info_fechamento = input("Digite o novo horário de fechamento: ")

            nova_info_funciona_fds = input("Funciona aos finais de semana? (s/n): ").lower()

            if nova_info_funciona_fds == 's':
                nova_info_funciona_fds = True
            elif nova_info_funciona_fds == 'n':        
                nova_info_funciona_fds = False
            else:
                print("Entrada inválida para funcionamento aos finais de semana. Por favor, digite 's' para sim ou 'n' para não.")
                return

            unidade["horario_funcionamento"] = {
                "abertura": nova_info_abertura,
                "fechamento": nova_info_fechamento,
                "funciona_fds": nova_info_funciona_fds
            }
    else:
        print("Unidade não encontrada.")

# Função resposável por deletar o carregador
def deletar_unidade(id_unidade):
    unidade = dados.get("unidades", {}).get(id_unidade)
    if unidade:
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