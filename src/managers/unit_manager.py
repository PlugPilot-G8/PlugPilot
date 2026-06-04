# unit_manager.py - Gerenciamento e CRUD das unidades

from .database_manager import carregar_database, atualizar_database
from ..services.service import gerar_id, buscar_cep_info

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
def listar_unidade(id_unidade):
    from .chager_manager import listar_carregador, gerenciar_carregadores

    unidades = dados.get("unidades", {})
    carregadores = dados.get("carregadores", {})

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
                listar_carregador(carregador["id_carregador"])

        if not encontrou_carregador:
            print("Nenhum carregador cadastrado nessa unidade.")

        print(f"------------------------------ Gerenciar Unidade --------------------------------------")
        while True:
            print("\nO que deseja fazer?")
            print("\n1. Editar Unidade")
            print("2. Deletar Unidade")
            print("3. Gerenciar Carregadores")
            print("4. Voltar")

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
                gerenciar_carregadores(id_unidade)
            elif opcao == "4":
                break
            else:
                print("Opção inválida.")
    else:
        print("Unidade não encontrada.")

def listar_unidades(id_usuario):
    unidades = dados.get("unidades", {})
    unidades_usuario = [unidade for unidade in unidades.values() if unidade["id_dono"] == id_usuario]

    if unidades_usuario:
        for i, unidade in enumerate(unidades_usuario, start=1):
            print(f"{i}. {unidade['nome_unidade']}")
    else:
        print("Nenhuma unidade cadastrada por você.")

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