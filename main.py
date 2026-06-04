# main.py - Responsável por iniciar o sistema e criar a base de dados, se necessário.

import threading

from src.managers.database_manager import carregar_database
from src.managers.chager_manager import atualizar_status_por_hardware
from src.services.serial_service import SerialService
from src.services.service import obter_localizacao_usuario
from src.ui.geral_ui import menu_principal

PORTA_ARDUINO = "COM10"
BAUD_RATE = 9600

if __name__ == "__main__":
    print("[MAIN] Inicializando Sistema...")

    try:
        carregar_database()
    except Exception as erro:
        print(f"[MAIN] Erro ao carregar o banco de dados: {erro}")

    serial_service = SerialService(
        porta=PORTA_ARDUINO,
        baud_rate=BAUD_RATE,
        atualizar_status_callback=atualizar_status_por_hardware
    )

    serial_service.conectar()

    thread_serial = threading.Thread(
        target=serial_service.escutar,
        daemon=True
    )

    thread_serial.start()

    menu_principal()