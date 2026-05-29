# main.py - Responsável por iniciar o sistema e criar a base de dados, se necessário.

from src.managers.database_manager import carregar_database
from src.ui.terminal_ui import menu_principal

if __name__ == "__main__":
    print("[MAIN] Inicializando Sistema...")
    try:
        dados = carregar_database()
    except Exception as erro:
        print(f"[MAIN] Erro ao carregar o banco de dados: {erro}")
        dados = None
        
    menu_principal()