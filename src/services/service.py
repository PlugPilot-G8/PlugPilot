import random
import requests
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
    cep_limpo = "".join(filter(str.isdigit, str(cep)))
    
    # Valores padrão caso a busca falhe ou o CEP seja inválido
    endereco_formatado = f"Endereço para o CEP {cep} (informação não disponível)"
    latitude, longitude = -23.550520, -46.633309 # Centro de São Paulo
    
    if len(cep_limpo) == 8:
        try:
            # Busca o endereço real
            url_viacep = f"https://viacep.com.br/ws/{cep_limpo}/json/"
            resposta_cep = requests.get(url_viacep, timeout=5)
            dados_cep = resposta_cep.json()
            
            if "erro" not in dados_cep:
                logradouro = dados_cep.get("logradouro", "")
                bairro = dados_cep.get("bairro", "")
                cidade = dados_cep.get("localidade", "")
                estado = dados_cep.get("uf", "")
                
                endereco_formatado = f"{logradouro}, {bairro}, {cidade} - {estado}, Brazil"
                
                # Busca as coordenadas reais
                url_nominatim = "https://nominatim.openstreetmap.org/search"
                parametros = {"q": endereco_formatado, "format": "json", "limit": 1}
                headers = {"User-Agent": "ProjetoFaculdadeJunho2026/1.0 (teste@faculdade.edu)"}
                
                resposta_geo = requests.get(url_nominatim, params=parametros, headers=headers, timeout=5)
                dados_geo = resposta_geo.json()
                
                if dados_geo:
                    latitude = float(dados_geo[0]["lat"])
                    longitude = float(dados_geo[0]["lon"])
        except Exception:
            # Em caso de qualquer erro, os valores padrão serão usados.
            pass

    # Retorna o endereço formatado e as coodernadas
    return {
        "endereco_formatado": endereco_formatado,
        "coordenadas": {
            "latitude": latitude,
            "longitude": longitude
        }
    }