# unit_manager.py - Gerenciamento e CRUD das unidades

from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id, buscar_cep_info
from math import radians, cos, sin, asin, sqrt

dados =  carregar_database()

# Função para criar uma nova unidade
def cadastrar_unidade(id_dono):
    unidades = dados.get("unidades", {})

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
def listar_unidade(id_usuario, id_unidade):
    from .chager_manager import visualizar_carregadores, visualizar_carregador, gerenciar_carregadores, buscar_id, obter_vagas_unidade
    
    # Garante a carga dos dados atualizados
    dados = carregar_database()
    unidades = dados.get("unidades", {})
    carregadores = dados.get("carregadores", {})

    unidade = unidades.get(id_unidade)
    usuario = dados.get("usuarios", {}).get(id_usuario)

    if unidade:
        # CALCULO DINÂMICO DE VAGAS
        vagas = obter_vagas_unidade(id_unidade, dados)

        print(f"-------------------- {unidade['nome_unidade']} --------------------")
        print(f"Endereço: {unidade['endereco_formatado']}")
        print(f"Horário de Funcionamento: {unidade['horario_funcionamento']['abertura']} - {unidade['horario_funcionamento']['fechamento']}")
        print(f"Funciona aos Finais de Semana: {'Sim' if unidade['horario_funcionamento']['funciona_fds'] else 'Não'}")
        print(f"Avaliação Média: {unidade['avaliacao_media']}")
        print(f"Status: {unidade['status']}")
        print(f"Vagas Disponíveis: {vagas}")
        print("----------------------------------------------------------------------")

        print("\nCarregadores:")

        visualizar_carregadores(id_unidade)
        
        if usuario["tipo_usuario"] == "motorista":
            while True:
                print("----------------------------------------------------------------------")
                print("1. Visualizar Carregador")
                print("2. Voltar")
                print("----------------------------------------------------------------------")
                
                opcao = input("Escolha uma opção: ")
                
                if opcao == "1":
                    nome_carregador = input("Carregador que deseja visualizar: ")
                    id_carregador = buscar_id(nome_carregador, id_unidade)
                    
                    if id_carregador:
                        visualizar_carregador(id_usuario, id_carregador)
                    else:
                        print("Carregador não encontrado.")
                        
                elif opcao == "2":
                    break
                
        elif usuario["tipo_usuario"] == "empresario":
            while True:
                print("----------------------------------------------------------------------")
                print("1. Editar Unidade")
                print("2. Deletar Unidade")
                print("3. Gerenciar Carregadores")
                print("4. Voltar")
                print("----------------------------------------------------------------------")
                
                opcao = input("Escolha uma opção: ")
                
                if opcao == "1":
                    print("\nO que deseja alterar?")
                    print("1. Nome da Unidade")
                    print("2. CEP")
                    print("3. Horário de Funcionamento")
                    
                    opcao = input("Escolha uma opção: ")
                    
                    if opcao == "1":
                        editar_unidade(id_unidade, "nome_unidade")
                    elif opcao  == "2":
                        editar_unidade(id_unidade, "CEP")
                    elif opcao == "3":
                        editar_unidade(id_unidade, "horario_funcionamento")
                    else:
                        print("Opção inválida.")
                
                elif opcao == "2":
                    deletar_unidade(id_unidade)
                    break
                
                elif opcao == "3":
                    gerenciar_carregadores(id_usuario, id_unidade)
                    
                elif opcao == "4":
                    break
                else:
                    print("Opção inválida.")

def listar_unidades(id_usuario):
    from .chager_manager import obter_vagas_unidade
    
    dados = carregar_database()
    unidades = dados.get("unidades", {})
    unidades_usuario = [unidade for unidade in unidades.values() if unidade["id_dono"] == id_usuario]

    if unidades_usuario:
        print("\n=== Suas Unidades Cadastradas ===")
        for i, unidade in enumerate(unidades_usuario, start=1):
            vagas = obter_vagas_unidade(unidade["id_unidade"], dados)
            print(f"{i}. {unidade['nome_unidade']} - Vagas: {vagas}")
    else:
        print("Nenhuma unidade cadastrada por você.")

def listar_unidades_proximas(id_usuario, raio_max_km=20.0):
    from .chager_manager import obter_vagas_unidade
    
    dados = carregar_database()
    usuarios = dados.get("usuarios", {})
    usuario = usuarios.get(id_usuario)
    
    if not usuario:
        print("Usuário não encontrado.")
        return

    coordenadas_usuario = usuario.get("coordenadas_atual")
    if not coordenadas_usuario:
        print("Coordenadas do usuário não encontradas.")
        return

    unidades = dados.get("unidades", {})
    unidades_proximas = []

    for unidade in unidades.values():
        coordenadas_unidade = unidade.get("coordenadas")
        if coordenadas_unidade:
            distancia = calcular_distancia(coordenadas_usuario, coordenadas_unidade)
            
            if distancia <= raio_max_km:
                unidades_proximas.append((unidade, distancia))

    unidades_proximas.sort(key=lambda x: x[1])

    print(f"\n=== Estações a até {raio_max_km}km de você ===")
    if not unidades_proximas:
        print("Nenhuma estação encontrada nessa região.")
        return

    for unidade, distancia in unidades_proximas:
        vagas = obter_vagas_unidade(unidade["id_unidade"], dados)
        
        print(f"-> {unidade['nome_unidade']}")
        print(f"   Distância: {distancia:.2f} km")
        print(f"   Vagas disponíveis: {vagas}") # <-- Inserido com sucesso aqui também
        print(f"   Status: {unidade['status']} | Avaliação: ⭐ {unidade['avaliacao_media']}\n")

def calcular_distancia(coordenadas_usuario, coordenadas_unidade):
    lat1 = coordenadas_usuario["latitude"]
    lon1 = coordenadas_usuario["longitude"]
    lat2 = coordenadas_unidade["latitude"]
    lon2 = coordenadas_unidade["longitude"]

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

# Função para editar as informações de uma unidade existente
def editar_unidade(id_unidade, alteracao):
    unidades = dados.get("unidades", {})
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