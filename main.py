# main.py - Responsável por iniciar o sistema e criar a base de dados, se necessário.

from src.database_manager import carregar_database, criar_database
from src.app import menu_principal

if __name__ == "__main__":
    print("[MAIN] Inicializando Sistema...")
    try:
        dados = carregar_database()
    except Exception as erro:
        print(f"[MAIN] Erro ao carregar o banco de dados: {erro}")
        dados = None

    if dados == False:
        try:
            criar_database()
        except Exception as erro:
            print(f"[MAIN] Erro ao criar o banco de dados: {erro}")
            exit(1) 
        criar_database()
    menu_principal()