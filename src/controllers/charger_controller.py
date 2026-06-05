# src/controllers/charger_controller.py

from datetime import datetime, timedelta
from ..managers.reserve_manager import obter_comando_estado_carregador, validar_liberacao_por_codigo

# Variável global para armazenar a instância da classe SerialService iniciada no main
_serial_service_instance = None

# Cache para armazenar os tokens/códigos ativos enviados pelo Arduino
codigos_ativos = {}

def registrar_servico_serial(instancia_serial):
    """Guarda a instância da classe SerialService criada no main.py."""
    global _serial_service_instance
    _serial_service_instance = instancia_serial

def sincronizar_hardware_com_banco(id_carregador="chg_001"):
    """Consulta as reservas no JSON e atualiza o display do Arduino."""
    global _serial_service_instance
    if not _serial_service_instance:
        print("[Controlador] Alerta: Nenhum serviço serial registrado ainda.")
        return

    # Pega o comando baseado no banco (ex: "RESERVED:chg_001" ou "FREE:chg_001")
    comando = obter_comando_estado_carregador(id_carregador) 
    
    # Envia para o Arduino em letras maiúsculas (ex: RESERVED:CHG001)
    # IMPORTANTE: Garanta que o método de enviar na sua classe se chama 'enviar_comando'
    _serial_service_instance.enviar_comando(comando.upper())

def processar_codigo_recebido(id_carregador, codigo):
    """Salva o código gerado pelo Arduino na memória global."""
    id_json = id_carregador.lower()  # Garante que CHG001 vire chg_001
    codigos_ativos[id_json] = {
        "codigo": str(codigo),
        "expira_em": datetime.now() + timedelta(minutes=5)
    }
    print(f"\n[Hardware] Token {codigo} guardado para o carregador {id_carregador}.")

def tentar_liberacao_totem(id_motorista, codigo_digitado, id_carregador="chg_001"):
    """Valida os dados e, se correto, manda o ALLOW para a serial."""
    global _serial_service_instance
    if not _serial_service_instance:
        print("[Controlador] Erro: Serial não disponível.")
        return False

    # Chama a sua função original de validação do reserve_manager
    permitido, mensagem = validar_liberacao_por_codigo(
        id_carregador=id_carregador,
        id_motorista=id_motorista,
        codigo_digitado=codigo_digitado,
        codigos_ativos=codigos_ativos
    )
    
    print(f"\n[Validação] Resultado: {mensagem}")
    
    if permitido:
        _serial_service_instance.enviar_comando(f"ALLOW:{id_carregador.upper()}")
        if id_carregador in codigos_ativos:
            del codigos_ativos[id_carregador]
        return True
    else:
        _serial_service_instance.enviar_comando(f"DENY:{id_carregador.upper()}")
        return False