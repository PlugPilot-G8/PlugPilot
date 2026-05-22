# DataBaseManager.py - Responsável por criar e carregar a base de dados do sistema.

import json

def criar_database():
    dados = {
        "usuarios": {
            "usr_001": {
                "id_usuario": "usr_001",
                "nome": "Carlos Empresário",
                "tipo_usuario": "empresario",
                "documento": "12.345.678/0001-99",
                "email": "empresa@gmail.com",
                "senha": "empresa123",
                "telefone": "+5511999998888",
                "data_cadastro": "2026-01-15T10:30:00Z"
            },
            "usr_002": {
                "id_usuario": "usr_002",
                "nome": "Lucas Motorista",
                "tipo_usuario": "motorista",
                "documento": "123.456.789-00",
                "email": "user@gmail.com",
                "senha": "user123",
                "telefone": "+5511988887777",
                "data_cadastro": "2026-02-10T14:22:00Z",
                "historico_reservas": [
                    "res_901"
                ]
            }
        },

        "unidades": {
            "und_001": {
                "id_unidade": "und_001",
                "id_dono": "usr_001",
                "nome_unidade": "PlugPilot Station - Jardins",
                "endereco_formatado": "Alameda Lorena, 1234 - Jardins, São Paulo - SP, 01424-001",
                "coordenadas": {
                    "latitude": -23.561684,
                    "longitude": -46.662083
                },
                "horario_funcionamento": {
                    "abertura": "07:30",
                    "fechamento": "22:00",
                    "funciona_fds": True
                },
                "avaliacao_media": 4.8
            }
        },

        "carregadores": {
            "chg_001": {
                "id_carregador": "chg_001",
                "id_unidade": "und_001",
                "modelo": "Volvo Wallbox Plus",
                "fabricante": "Volvo",
                "tipo_corrente": "AC",
                "potencia_kw": 22.0,
                "tipo_conector": "Tipo 2 (Europeu)",
                "preco_por_kwh": 2.49,
                "status_atual": "Disponivel",
                "ultima_manutencao": "2026-04-01",
                "recursos": {
                    "permite_reserva": True,
                    "fila_virtual": True,
                    "plug_and_charge": False
                }
            }
        },

        "reservas": {
            "res_901": {
                "id_reserva": "res_901",
                "id_motorista": "usr_002",
                "id_unidade": "und_001",
                "id_carregador": "chg_001",
                "status_reserva": "Concluida",
                "agendado_para": "2026-05-21T16:00:00Z",
                "duracao_minutos": 60,
                "valor_estimado": 45.80,
                "kwh_consumido": 18.4
            }
        }
    }

    with open("banco.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    print("Banco inicial criado com sucesso!")

def carregar_database():
    try:
        with open("banco.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados
    except FileNotFoundError:
        print("Arquivo de banco de dados não encontrado. Criando um novo banco...")
        criar_database()
        return carregar_database()
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo de banco de dados. Criando um novo banco...")
        criar_database()
        return carregar_database()
    
def atualizar_database(dados):
    with open("banco.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)