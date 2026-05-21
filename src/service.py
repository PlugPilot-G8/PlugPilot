# service.py - Responsável por fornecer as funções de serviço para o sistema, como login, cadastro, controle de unidades e dispositivos.

# Responsavel por gerenciar os carregadores (CRUD)
import json
from database_manager import carregar_database, atualizar_database

dados = carregar_database()
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

# Responsavel por gerenciar os carregadores (CRUD)

units = dados.get("unidades", {})

# Função responsável por criar um novo carregador
def gerar_id_unidade():
    return f"und_{len(units) + 1:03d}"

def buscar_cep_info(cep):
    # Simulação de busca de informações do CEP
    # Em um cenário real, você poderia usar uma API externa para obter essas informações
    return {
        "endereco_formatado": f"Endereço formatado para CEP {cep}",
        "coordenadas": {
            "latitude": -23.561684,
            "longitude": -46.625378
        }
    }

def criar_unidade(id_dono):
    # Gerar um ID único para a nova unidade
    id_unidade = gerar_id_unidade()

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

criar_unidade("usr_001")

# Função responsável por exibir o carregador
def visualizar_unidade(id_unidade):
    unit = units.get(id_unidade)
    if unit:
        print(f"Unidade: {unit['nome_unidade']}")
    else:
        print("Unidade não encontrada.")

# Função responsável por editar o carregador
def editar_unidade():
    print("editando unidade...")

# Função resposável por deletar o carregador
def deletar_unidade():
    print("deletando unidade...")

