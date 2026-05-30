

import random
from datetime import datetime

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