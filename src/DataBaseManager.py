import json

def criar_database():
    dados = {
        "usuarios": {

            "admin": {
                "nome": "Administrador",
                "id_usuario": 0,
                "tipo_usuario": "admin",
                "email": "admin@gmail.com",
                "senha": "admin123"
            },

            "empresario": {
                "nome": "Carlos Empresário",
                "id_usuario": 1,
                "tipo_usuario": "empresario",
                "email": "empresa@gmail.com",
                "senha": "empresa123",

                "reservas": {},

                "unidades": {
                    "unidade1": {
                        "nome": "PlugPilot Station",
                        "localizacao": "Rua Template, 000",
                        "horario_abertura": 7.30,
                        "horario_fechamento": 22.00,

                        "carregadores": {
                            "carregador1": {
                                "nome": "Carregador 1",
                                "preco": 7.4,
                                "potencia_maxima": 12,
                                "tipo": "Inteligente",
                                "status_operacional": "Disponível",

                                "permissoes": {
                                    "reserva": True,
                                    "mapa_publico": True,
                                    "fila_inteligente": True
                                }
                            }
                        }
                    }
                }
            },

            "motorista": {
                "nome": "Lucas Motorista",
                "id_usuario": 2,
                "tipo_usuario": "motorista",
                "email": "user@gmail.com",
                "senha": "user123",

                "reservas": {
                    "reserva1": {
                        "unidade": "unidade1",
                        "data": "",
                        "horario": "",
                        "duracao_estimada": ""
                    }
                }
            }
        }
    }

    with open("banco.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    print("Banco inicial criado com sucesso!")