# main.py - Responsável por iniciar o sistema e criar a base de dados, se necessário.

from src.DataBaseManager import criar_database
from src.app import menu_principal

if __name__ == "__main__":
    print("[MAIN] Inicializando Sistema...")
    try:
        criar_database()
    except Exception as erro:
        print(f"[MAIN] Erro ao inicializar o sistema: {erro}")
    
    menu_principal()