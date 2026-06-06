# charger_controller.py - Gerenciamento de estado lógico e comunicação com o Totem

from datetime import datetime, timedelta
from ..managers.reserve_manager import obter_comando_estado_carregador, validar_liberacao_por_codigo

_serial_service_instance = None

codigos_ativos = {}

def registrar_servico_serial(instancia_serial):
    global _serial_service_instance
    _serial_service_instance = instancia_serial

def sincronizar_hardware_com_banco(id_carregador="chg_001"):
    global _serial_service_instance
    
    if not _serial_service_instance:
        print("[Controlador] Alerta: Nenhum serviço serial registrado ainda.")
        return

    comando = obter_comando_estado_carregador(id_carregador) 
    _serial_service_instance.enviar_comando(comando.upper())

def processar_codigo_recebido(id_carregador, codigo):

    id_normalizado = id_carregador.strip().lower()
    
    codigos_ativos[id_normalizado] = {
        "codigo": str(codigo),
        "expira_em": datetime.now() + timedelta(minutes=5)
    }
    print(f"\n[Hardware] Token {codigo} guardado para o carregador {id_carregador}.")

def tentar_liberacao_totem(id_motorista, codigo_digitado, id_carregador="chg_001"):
    global _serial_service_instance
    
    if not _serial_service_instance:
        print("[Controlador] Erro: Serial não disponível.")
        return False

    id_normalizado = id_carregador.strip().lower()

    permitido, mensagem = validar_liberacao_por_codigo(
        id_carregador=id_carregador,
        id_motorista=id_motorista,
        codigo_digitado=codigo_digitado,
        codigos_ativos=codigos_ativos
    )
    
    print(f"\n[Validação] Resultado: {mensagem}")
    
    if permitido:
        _serial_service_instance.enviar_comando(f"ALLOW:{id_carregador.upper()}")

        if id_normalizado in codigos_ativos:
            del codigos_ativos[id_normalizado]
        return True
    else:
        _serial_service_instance.enviar_comando(f"DENY:{id_carregador.upper()}")
        return False