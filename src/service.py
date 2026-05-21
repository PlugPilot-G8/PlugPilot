# service.py - Responsável por fornecer as funções de serviço para o sistema, como login, cadastro, controle de unidades e dispositivos.

# Responsavel por gerenciar os carregadores (CRUD)
import json

with open("banco.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

chargers = dados.get("carregadores", {})

# carregar banco de dados
# Coletar informações
# Validar as informações
# Salvar as informações no banco de dados

# Função responsável por criar um novo carregador
def criar_carregador(chargers):
    id_carregador = input("Digite o ID do carregador: ")
    if id_carregador in chargers:
        print("ID de carregador já existe. Por favor, escolha um ID diferente.")
        return

    id_unidade = input("Digite o ID da unidade associada: ")
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
    
    print("criando carregador...")

criar_carregador(chargers)

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

# Responsavel por gerenciar os carregadores (CRUD)

units = dados.get("unidades", {})

# Função responsável por criar um novo carregador
def criar_unidade():
    print("criando unidade...")

# Função responsável por exibir o carregador
def visualizar_unidade(id_unidade):
    unit = units.get(id_unidade)
    if unit:
        print(f"Unidade: {unit['nome_fantasia']}")
    else:
        print("Unidade não encontrada.")

# Função responsável por editar o carregador
def editar_unidade():
    print("editando unidade...")

# Função resposável por deletar o carregador
def deletar_unidade():
    print("deletando unidade...")

