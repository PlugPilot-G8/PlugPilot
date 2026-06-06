# service.py - Utilitários, geolocalização e serviços do sistema via SQLite

import random
import requests
import geocoder
from datetime import datetime
from ..managers.database_manager import conectar

TIPOS = {
    "carregador": (0, 30),
    "unidade": (31, 50),
    "usuario": (51, 70),
    "reserva": (71, 99)
}

def gerar_id(tipo):
    if tipo not in TIPOS:
        raise ValueError("Tipo inválido")

    inicio, fim = TIPOS[tipo]
    prefixo = random.randint(inicio, fim)
    horario = datetime.now().strftime("%H%M%S")

    return f"{prefixo:02}{horario}"

def buscar_cep_info(cep):
    cep_limpo = "".join(filter(str.isdigit, str(cep)))
    

    endereco_formatado = f"Endereço para o CEP {cep} (informação não disponível)"
    latitude, longitude = -23.550520, -46.633309
    
    if len(cep_limpo) == 8:
        try:

            url_viacep = f"https://viacep.com.br/ws/{cep_limpo}/json/"
            resposta_cep = requests.get(url_viacep, timeout=5)
            dados_cep = resposta_cep.json() if hasattr(resposta_cep, 'json') else resposta_cep.json()
            dados_cep = resposta_cep.json()
            
            if "erro" not in dados_cep:
                logradouro = dados_cep.get("logradouro", "")
                bairro = dados_cep.get("bairro", "")
                cidade = dados_cep.get("localidade", "")
                estado = dados_cep.get("uf", "")
                
                endereco_formatado = f"{logradouro}, {bairro}, {cidade} - {estado}, Brazil"
                
                url_nominatim = "https://nominatim.openstreetmap.org/search"
                parametros = {"q": endereco_formatado, "format": "json", "limit": 1}
                headers = {"User-Agent": "ProjetoFaculdadeJunho2026/1.0 (teste@faculdade.edu)"}
                
                resposta_geo = requests.get(url_nominatim, params=parametros, headers=headers, timeout=5)
                dados_geo = resposta_geo.json()
                
                if dados_geo:
                    latitude = float(dados_geo[0]["lat"])
                    longitude = float(dados_geo[0]["lon"])
        except Exception:
            pass

    return {
        "endereco_formatado": endereco_formatado,
        "coordenadas": {
            "latitude": latitude,
            "longitude": longitude
        }
    }

def obter_localizacao_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    if cursor.fetchone()[0] == 0:
        print(f"[ERRO] Usuário {id_usuario} não encontrado no banco de dados.")
        conn.close()
        return

    g = geocoder.ip('me')
    
    if g.latlng:
        lat_detectada, lng_detectada = g.latlng
        
        cursor.execute("""
            UPDATE usuarios 
            SET latitude = ?, longitude = ? 
            WHERE id_usuario = ?
        """, (lat_detectada, lng_detectada, id_usuario))
        
        conn.commit()
    else:
        print("\n[AVISO] Falha ao rastrear IP. Mantendo coordenadas padrões do Banco.")
        
    conn.close()