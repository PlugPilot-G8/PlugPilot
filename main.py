# main.py - Responsável por iniciar o sistema e criar a base de dados SQLite se necessário.

import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.managers.database_manager import criar_tabelas
from src.managers.charger_manager import atualizar_status_por_hardware
from src.managers.reserve_manager import obter_comando_estado_carregador
from src.services.serial_service import SerialService
from src.ui.geral_ui import menu_principal

PORTA_ARDUINO = "COM10"
BAUD_RATE = 9600

if __name__ == "__main__":
    print("[MAIN] Inicializando Sistema PlugPilot...")

    try:
        criar_tabelas()
        print("[MAIN] Banco de dados SQLite verificado/criado com sucesso.")
    except Exception as erro:
        print(f"[MAIN] Erro crítico ao inicializar o banco de dados SQLite: {erro}")
        sys.exit(1)

    serial_service = SerialService(
        porta=PORTA_ARDUINO,
        baud_rate=BAUD_RATE,
        atualizar_status_callback=atualizar_status_por_hardware,
        obter_estado_reserva_callback=obter_comando_estado_carregador
    )

    serial_service.conectar()

    thread_serial = threading.Thread(
        target=serial_service.escutar,
        daemon=True
    )
    thread_serial.start()

    menu_principal(serial_service)