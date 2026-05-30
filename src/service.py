# service.py - Responsável por implementar as funcionalidades de criação, visualização, edição e exclusão de carregadores e unidades.

import json
import random
from datetime import datetime
from .database_manager import carregar_database, atualizar_database
from .validator import validar_email, validar_senha, validar_cpf, validar_cnpj, validar_telefone, validar_nome
from .app1 import menu_motorista, menu_empresario

# Carrega os dados do banco de dados
dados = carregar_database()

# Garante que as chaves "usuarios", "carregadores" e "unidades" existam no dicionário de dados
usuarios = dados.get("usuarios", {})
dados.setdefault("carregadores", {})
dados.setdefault("unidades", {})

#Geradores de ID para diferentes tipos de entidades no sistema.
TIPOS = {
    "carregador": (0, 30),
    "unidade": (31, 50),
    "usuario": (51, 70),
    "reserva": (71, 99)
}

# Função para gerar IDs únicos para diferentes tipos de entidades no sistema
def gerar_id(tipo):
    if tipo not in TIPOS:
        raise ValueError("Tipo inválido")

    inicio, fim = TIPOS[tipo]
    prefixo = random.randint(inicio, fim)
    horario = datetime.now().strftime("%H%M%S")

    return f"{prefixo:02}{horario}"

# Função para buscar informações de endereço e coordenadas com base no CEP fornecido
def buscar_cep_info(cep):
    #gera dados aleatórios para endereço e coordenadas, já que não é possível fazer requisições externas para obter informações reais de CEP
    endereco_formatado = f"Endereço formatado para CEP {cep}"
    coordenadas = {
        "latitude": random.uniform(-23.0, -22.0),  # Gerar latitude aleatória dentro de um intervalo
        "longitude": random.uniform(-46.0, -45.0)  # Gerar longitude aleatória dentro de um intervalo
    }
    
    return {
        "endereco_formatado": endereco_formatado,
        "coordenadas": {
            "latitude": coordenadas["latitude"],
            "longitude": coordenadas["longitude"]
        }
    }
    
# Usuarios

# Função para realizar o login de um usuário
def login(tipo_usuario):
    # Recebe e valida as informações do usuário
    email = input("Email: ")
    if not validar_email(email):
        print("Email inválido! Por favor, tente novamente.")
        return
    
    senha = input("Senha: ")
    if not validar_senha(senha):
        print("Senha inválida! Por favor, tente novamente.")
        return
    
    if tipo_usuario== "motorista":
        documento=input("Digite o seu CPF: ")
        if not validar_cpf(documento):
            print("CPF inválido! Por favor, tente novamente.")
            return
    
    elif tipo_usuario=="empresario":
        documento=input("Digite o seu CNPJ: ")
        if not validar_cnpj(documento):
            print("CNPJ inválido! Por favor, tente novamente.")
            return
    else:
        print("Tipo de usuário inválido! Por favor, tente novamente.")
        return

    # Verifica as credenciais do usuário no banco de dados, comparando o email, senha e documento fornecidos com os registros existentes
    for usuario in usuarios.values():
        if usuario["email"] == email and usuario["senha"] == senha and usuario["documento"]==documento:

            print(f"\nBem-vindo {usuario['nome']}!")
            if usuario["tipo_usuario"] == "motorista":
                menu_motorista()
            elif usuario["tipo_usuario"] == "empresario":
                menu_empresario()
            return

    print("Email ou senha incorretos!")
    return None

# Função para cadastrar um novo usuário (empresário ou motorista)
def cadastrar_usuario(tipo_usuario):
    # Recebe e valida as informações do usuário
    nome = input("Nome: ")
    if not validar_nome(nome):
        print("Nome inválido! Por favor, tente novamente.")
        return
    
    email = input("Email: ")
    if not validar_email(email):
        print("Email inválido! Por favor, tente novamente.")
        return
    
    for usuario in dados["usuarios"].values():
        if usuario["email"] == email:
            print("Email já cadastrado!")
            return
    
    if tipo_usuario == "motorista":
        documento = input("CPF: ")
        if not validar_cpf(documento):
            print("CPF inválido! Por favor, tente novamente.")
            return
    
    elif tipo_usuario == "empresario":
        documento = input("CNPJ: ")
        if not validar_cnpj(documento):
            print("CNPJ inválido! Por favor, tente novamente.")
            return
        
    senha = input("Senha: ")
    if not validar_senha(senha):
        print("Senha inválida! Por favor, tente novamente.")
        return
    
    telefone = input("Telefone: ")
    if not validar_telefone(telefone):
        print("Telefone inválido! Por favor, tente novamente.")
        return

    id_usuario = gerar_id("usuario")

    novo_usuario = {
        "id_usuario": id_usuario,
        "nome": nome,
        "tipo_usuario": tipo_usuario,
        "documento": documento,
        "email": email,
        "senha": senha,
        "telefone": telefone,
        "data_cadastro": datetime.now().isoformat(),
        "historico_reservas": []
    }

    dados["usuarios"][id_usuario] = novo_usuario

    atualizar_database(dados)

    print("Usuário cadastrado com sucesso!")

# Função para atualizar as informações de um usuário existente
def atualizar_usuario(id_usuario, alteracao):
    # Verifica se o usuário existe no banco de dados
    if id_usuario not in dados["usuarios"]:
        print("Usuário não encontrado!")
        return

    # Obtém as informações do usuário a ser atualizado
    usuario = dados["usuarios"][id_usuario]
    tipo_usuario = usuario["tipo_usuario"]

    # Recebe a nova informação a ser atualizada e valida de acordo com o tipo de alteração
    if alteracao=="nome":
        nova_info=input("Digite o novo nome: ")
        if usuario["nome"]==nova_info:
            print("Escolha um nome diferente do atual")
            return
        if not validar_nome(nova_info):
            print("Nome inválido! Por favor, tente novamente.")
            return
        usuario["nome"] = nova_info
    
    if alteracao=="documento":
        if usuario["documento"]==nova_info:
            print("Escolha um número de documento diferente do atual")
            return
        
        if tipo_usuario=="motorista":
            nova_info=input("CPF: ")
            if usuario["documento"]==nova_info:
                print("Escolha um CPF diferente do atual")
                return 
            if not validar_cpf(nova_info):
                print("CPF inválido! Por favor, tente novamente.")
                return
            
        if tipo_usuario=="empresario":
            nova_info=input("CNPJ: ")
            if usuario["documento"]==nova_info:
                print("Escolha um CNPJ diferente do atual")
                return
            if not validar_cnpj(nova_info):
                print("CNPJ inválido! Por favor, tente novamente.")
                return
        
        usuario["documento"]=nova_info

    if alteracao=="email":
        nova_info=input("Digite um novo email: ")
        if usuario["email"]==nova_info:
            print("Escolha um email diferente do atual")
            return
        if not validar_email(nova_info):
            print("Email inválido! Por favor, tente novamente.")
            return
        if nova_info in [usuario.get("email") for usuario in usuarios.values()]:
                print("Email já cadastrado para outro usuário. Por favor, verifique o email e tente novamente.")
                return
        usuario["email"]=nova_info
    
    if alteracao=="senha":
        nova_info=input("Digite uma nova senha: ")
        if usuario["senha"]==nova_info:
            print("Escolha uma senha diferente da atual")
            return
        if not validar_senha(nova_info):
            print("Senha inválida! Por favor, tente novamente.")
            return
        usuario["senha"]=nova_info
    
    if alteracao=="telefone":
        nova_info=input("Digite um novo telefone: ")
        if usuario["telefone"]==nova_info:
            print("Escolha um telefone diferente do atual")
            return
        if not validar_telefone(nova_info):
            print("Telefone inválido! Por favor, tente novamente.")
            return
        usuario["telefone"]=nova_info

    # Atualiza as informações do usuário no banco de dados
    atualizar_database(dados)

    print("Usuário atualizado com sucesso!")

# Função para visualizar as informações de um usuário específico
def visualizar_usuario(id_usuario):
    # Verifica se o usuário existe no banco de dados
    if id_usuario not in dados["usuarios"]:
        print("Usuário não encontrado!")
        return

    usuario= usuarios.get(id_usuario)
    # Exibe as informações do usuário de forma formatada
    print("\n====== PERFIL USUÁRIO ======")
    print('Nome: ', usuario['nome'])
    print('Email: ', usuario['email'])
    print('Tipo de usuário: ', usuario['tipo_usuario'])
    print('Documento: ', usuario['documento'])
    print('Telefone: ', usuario['telefone'])
    print("\n============================")

# Função para deletar um usuário do sistema, verificando se o ID do usuário existe no banco de dados antes de realizar a exclusão
def deletar_usuario(id_usuario):

    if id_usuario in dados["usuarios"]:
        del dados["usuarios"][id_usuario]
        atualizar_database(dados)
        print("Usuário removido com sucesso!")
    else:
        print("Usuário não encontrado!")
        
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

# Unidades
unidades = dados.get("unidades", {})

# Função para criar uma nova unidade
def criar_unidade(id_dono):
    # Recebe e valida as informações da unidade
    nome_unidade = input("Digite o nome da unidade: ")
    if nome_unidade in [unidade.get("nome_unidade") for unidade in unidades.values()]:
        print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
        return

    cep = input("Digite o CEP da unidade: ")
    if cep in [unidade.get("CEP") for unidade in unidades.values()]:
        print("CEP já cadastrado para outra unidade. Por favor, verifique o CEP e tente novamente.")
        return

    abertura = input("Digite o horário de abertura: ")
    if not abertura:
        print("Horário de abertura é obrigatório. Por favor, tente novamente.")
        return

    fechamento = input("Digite o horário de fechamento: ")
    if not fechamento:
        print("Horário de fechamento é obrigatório. Por favor, tente novamente.")
        return

    funciona_fds = input("Funciona aos finais de semana? (s/n): ").lower()
    if funciona_fds == "s":
        funciona_fds = True
    elif funciona_fds == "n":
        funciona_fds = False
    else:
        print("Entrada inválida para funcionamento aos finais de semana.")
        return

    cep_info = buscar_cep_info(cep)
    id_unidade = gerar_id("unidade")

    # Atualiza as informações da unidade no banco de dados
    unidades.update({
        id_unidade: {
            "id_unidade": id_unidade,
            "id_dono": id_dono,
            "nome_unidade": nome_unidade,
            "CEP": cep,
            "endereco_formatado": cep_info["endereco_formatado"],
            "coordenadas": cep_info["coordenadas"],
            "horario_funcionamento": {
                "abertura": abertura,
                "fechamento": fechamento,
                "funciona_fds": funciona_fds
            },
            "avaliacao_media": 0.0
        }
    })

    atualizar_database(dados)
    print(f"Unidade {id_unidade} criada com sucesso.")

# Função para visualizar as informações de uma unidade específica
def visualizar_unidade(id_unidade):
    unidade = unidades.get(id_unidade)

    # Verifica se a unidade existe no banco de dados antes de exibir as informações
    if unidade:
        # Exibe as informações da unidade de forma formatada, incluindo os carregadores disponíveis na unidade
        print(f"-------------------- {unidade['nome_unidade']} --------------------")
        print(f"Endereço: {unidade['endereco_formatado']}")
        print(f"Horário de Funcionamento: {unidade['horario_funcionamento']['abertura']} - {unidade['horario_funcionamento']['fechamento']}")
        print(f"Funciona aos Finais de Semana: {'Sim' if unidade['horario_funcionamento']['funciona_fds'] else 'Não'}")
        print(f"Avaliação Média: {unidade['avaliacao_media']}")

        print("\nCarregadores:")

        encontrou_carregador = False

        # Exibe os carregadores disponíveis da unidade
        for carregador in carregadores.values():
            if carregador["id_unidade"] == id_unidade:
                encontrou_carregador = True
                visualizar_carregador(carregador["id_carregador"])

        if not encontrou_carregador:
            print("Nenhum carregador cadastrado nessa unidade.")

        print(f"--------------------------------------------------------------------")
    else:
        print("Unidade não encontrada.")

# Função para editar as informações de uma unidade existente
def editar_unidade(id_unidade, alteracao):
    unidade = dados.get("unidades", {}).get(id_unidade)

    # Verifica se a unidade existe no banco de dados antes de realizar as alterações
    if unidade:
        # Recebe a nova informação a ser atualizada e valida de acordo com o tipo de alteração
        print(f"Editando unidade: {unidade['nome_unidade']}")

        if alteracao == "nome_unidade":
            nova_info = input("Digite o novo nome da unidade: ")

            if nova_info in [unidade.get("nome_unidade") for unidade in unidades.values()]:
                print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
                return

            unidade["nome_unidade"] = nova_info

        if alteracao == "CEP":
            nova_info = input("Digite o novo CEP da unidade: ")

            if nova_info in [unidade.get("CEP") for unidade in unidades.values()]:
                print("CEP já cadastrado para outra unidade. Por favor, verifique o CEP e tente novamente.")
                return

            cep_info = buscar_cep_info(nova_info)

            unidade["CEP"] = nova_info
            unidade["endereco_formatado"] = cep_info["endereco_formatado"]
            unidade["coordenadas"] = cep_info["coordenadas"]

        if alteracao == "horario_funcionamento":
            nova_info_abertura = input("Digite o novo horário de abertura: ")
            nova_info_fechamento = input("Digite o novo horário de fechamento: ")

            nova_info_funciona_fds = input("Funciona aos finais de semana? (s/n): ").lower()

            if nova_info_funciona_fds == "s":
                nova_info_funciona_fds = True
            elif nova_info_funciona_fds == "n":
                nova_info_funciona_fds = False
            else:
                print("Entrada inválida para funcionamento aos finais de semana.")
                return

            unidade["horario_funcionamento"] = {
                "abertura": nova_info_abertura,
                "fechamento": nova_info_fechamento,
                "funciona_fds": nova_info_funciona_fds
            }

        # Atualiza as informações da unidade no banco de dados
        atualizar_database(dados)
        print("Unidade atualizada com sucesso.")

    else:
        print("Unidade não encontrada.")

# Função para deletar uma unidade do sistema
def deletar_unidade(id_unidade):
    unidade = dados.get("unidades", {}).get(id_unidade)

    if unidade:
        del dados["unidades"][id_unidade]
        atualizar_database(dados)
        print(f"Unidade {id_unidade} deletada com sucesso.")
    else:
        print("Unidade não encontrada.")