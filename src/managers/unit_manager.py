# unit_manager.py - Gerenciamento e CRUD das unidades via SQLite.

from .database_manager import conectar
from ..services.service import gerar_id, buscar_cep_info
from math import radians, cos, sin, asin, sqrt

# Função para criar uma nova unidade
def cadastrar_unidade(id_dono):
    nome_unidade = input("Digite o nome da unidade: ")
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Validação rápida de nome duplicado usando SQL
    cursor.execute("SELECT COUNT(*) FROM unidades WHERE nome_unidade = ?", (nome_unidade,))
    if cursor.fetchone()[0] > 0:
        print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
        conn.close()
        return

    cep = input("Digite o CEP da unidade: ")
    # Verifica duplicidade do CEP
    cursor.execute("SELECT COUNT(*) FROM unidades WHERE endereco_formatado LIKE ?", (f"%{cep}%",))
    if cursor.fetchone()[0] > 0:
        print("CEP já cadastrado para outra unidade. Por favor, verifique o CEP e tente novamente.")
        conn.close()
        return

    abertura = input("Digite o horário de abertura: ")
    if not abertura:
        print("Horário de abertura é obrigatório. Por favor, tente novamente.")
        conn.close()
        return

    fechamento = input("Digite o horário de fechamento: ")
    if not fechamento:
        print("Horário de fechamento é obrigatório. Por favor, tente novamente.")
        conn.close()
        return

    funciona_fds_input = input("Funciona aos finais de semana? (s/n): ").lower()
    if funciona_fds_input == "s":
        funciona_fds = 1
    elif funciona_fds_input == "n":
        funciona_fds = 0
    else:
        print("Entrada inválida para funcionamento aos finais de semana.")
        conn.close()
        return

    cep_info = buscar_cep_info(cep)
    id_unidade = gerar_id("unidade")
    
    latitude = cep_info["coordenadas"]["latitude"]
    longitude = cep_info["coordenadas"]["longitude"]
    endereco = cep_info["endereco_formatado"]

    cursor.execute("""
        INSERT INTO unidades (
            id_unidade, id_dono, status, nome_unidade, endereco_formatado, 
            latitude, longitude, abertura, fechamento, funciona_fds, avaliacao_media
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_unidade, id_dono, "Ativa", nome_unidade, endereco, latitude, longitude, abertura, fechamento, funciona_fds, 0.0))

    conn.commit()
    conn.close()
    print(f"Unidade {id_unidade} criada com sucesso.")

# Função para visualizar as informações de uma unidade específica
def listar_unidade(id_usuario, id_unidade, serial_service=None):
    from .charger_manager import visualizar_carregadores, visualizar_carregador, gerenciar_carregadores, buscar_id, obter_vagas_unidade
    
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM unidades WHERE id_unidade = ?", (id_unidade,))
    unidade_row = cursor.fetchone()
    
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    usuario = cursor.fetchone()
    conn.close()

    if not unidade_row:
        print("Unidade não encontrada.")
        return

    # Adaptador em tempo de execução para manter compatibilidade com a assinatura legada de dicionários aninhados nos menus
    unidade = {
        "id_unidade": unidade_row["id_unidade"],
        "id_dono": unidade_row["id_dono"],
        "status": unidade_row["status"],
        "nome_unidade": unidade_row["nome_unidade"],
        "endereco_formatado": unidade_row["endereco_formatado"],
        "avaliacao_media": unidade_row["avaliacao_media"] if "avaliacao_media" in unidade_row.keys() else unidade_row["avaliacao_media"] if hasattr(unidade_row, "keys") else unidade_row[10],
        "horario_funcionamento": {
            "abertura": unidade_row["abertura"],
            "fechamento": unidade_row["fechamento"],
            "funciona_fds": bool(unidade_row["funciona_fds"])
        }
    }
    # Pequena correção para garantir leitura robusta do índice ou chave de avaliação
    try:
        unidade["avaliacao_media"] = unidade_row["avaliacao_media"]
    except:
        unidade["avaliacao_media"] = 0.0

    vagas = obter_vagas_unidade(id_unidade)

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
                    visualizar_carregador(id_usuario, id_carregador, serial_service)
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
                
                opcao_edicao = input("Escolha uma opção: ")
                if opcao_edicao == "1":
                    editar_unidade(id_unidade, "nome_unidade")
                elif opcao_edicao == "2":
                    editar_unidade(id_unidade, "CEP")
                elif opcao_edicao == "3":
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
    from .charger_manager import obter_vagas_unidade
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unidades WHERE id_dono = ?", (id_usuario,))
    unidades_usuario = cursor.fetchall()
    conn.close()

    if unidades_usuario:
        print("\n=== Suas Unidades Cadastradas ===")
        for i, unidade in enumerate(unidades_usuario, start=1):
            vagas = obter_vagas_unidade(unidade["id_unidade"])
            print(f"{i}. {unidade['nome_unidade']} - Vagas: {vagas}")
    else:
        print("Nenhuma unidade cadastrada por você.")

def listar_unidades_proximas(id_usuario, raio_max_km=20.0):
    from .charger_manager import obter_vagas_unidade
    
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT latitude, longitude FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    usuario = cursor.fetchone()
    
    if not usuario or usuario["latitude"] is None:
        print("Coordenadas ou usuário não localizados.")
        conn.close()
        return

    coordenadas_usuario = {"latitude": usuario["latitude"], "longitude": usuario["longitude"]}

    cursor.execute("SELECT * FROM unidades")
    todas_unidades = cursor.fetchall()
    conn.close()

    unidades_proximas = []
    for unidade in todas_unidades:
        if unidade["latitude"] is not None and unidade["longitude"] is not None:
            coordenadas_unidade = {"latitude": unidade["latitude"], "longitude": unidade["longitude"]}
            distancia = calcular_distancia(coordenadas_usuario, coordenadas_unidade)
            
            if distancia <= raio_max_km:
                unidades_proximas.append((unidade, distancia))

    unidades_proximas.sort(key=lambda x: x[1])

    print(f"\n=== Estações a até {raio_max_km}km de você ===")
    if not unidades_proximas:
        print("Nenhuma estação encontrada nessa região.")
        return

    for unidade, distancia in unidades_proximas:
        vagas = obter_vagas_unidade(unidade["id_unidade"])
        print(f"-> {unidade['nome_unidade']}")
        print(f"   Distância: {distancia:.2f} km")
        print(f"   Vagas disponíveis: {vagas}")
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
    return c * 6371

def editar_unidade(id_unidade, alteracao):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM unidades WHERE id_unidade = ?", (id_unidade,))
    unidade = cursor.fetchone()

    if not unidade:
        print("Unidade não encontrada.")
        conn.close()
        return

    print(f"Editando unidade: {unidade['nome_unidade']}")

    if alteracao == "nome_unidade":
        nova_info = input("Digite o novo nome da unidade: ")
        cursor.execute("SELECT COUNT(*) FROM unidades WHERE nome_unidade = ? AND id_unidade != ?", (nova_info, id_unidade))
        if cursor.fetchone()[0] > 0:
            print("Nome de unidade já existe. Por favor, escolha um nome diferente.")
            conn.close()
            return
        cursor.execute("UPDATE unidades SET nome_unidade = ? WHERE id_unidade = ?", (nova_info, id_unidade))

    elif alteracao == "CEP":
        nova_info = input("Digite o novo CEP da unidade: ")
        cursor.execute("SELECT COUNT(*) FROM unidades WHERE endereco_formatado LIKE ? AND id_unidade != ?", (f"%{nova_info}%", id_unidade))
        if cursor.fetchone()[0] > 0:
            print("CEP já cadastrado para outra unidade.")
            conn.close()
            return
            
        cep_info = buscar_cep_info(nova_info)
        cursor.execute("""
            UPDATE unidades 
            SET endereco_formatado = ?, latitude = ?, longitude = ? 
            WHERE id_unidade = ?
        """, (cep_info["endereco_formatado"], cep_info["coordenadas"]["latitude"], cep_info["coordenadas"]["longitude"], id_unidade))

    elif alteracao == "horario_funcionamento":
        nova_info_abertura = input("Digite o novo horário de abertura: ")
        nova_info_fechamento = input("Digite o novo horário de fechamento: ")
        nova_info_funciona_fds = input("Funciona aos finais de semana? (s/n): ").lower()

        if nova_info_funciona_fds == "s":
            fds_val = 1
        elif nova_info_funciona_fds == "n":
            fds_val = 0
        else:
            print("Entrada inválida.")
            conn.close()
            return

        cursor.execute("""
            UPDATE unidades SET abertura = ?, fechamento = ?, funciona_fds = ? 
            WHERE id_unidade = ?
        """, (nova_info_abertura, nova_info_fechamento, fds_val, id_unidade))

    conn.commit()
    conn.close()
    print("Unidade atualizada com sucesso.")

def deletar_unidade(id_unidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM unidades WHERE id_unidade = ?", (id_unidade,))
    linhas = cursor.rowcount
    conn.commit()
    conn.close()

    if linhas > 0:
        print(f"Unidade {id_unidade} deletada com sucesso.")
    else:
        print("Unidade não encontrada.")