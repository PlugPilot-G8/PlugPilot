# user_manager.py - Gerenciamento e CRUD dos usuários via SQLite

from .database_manager import conectar
from ..validators.validator import validar_nome, validar_email, validar_senha, validar_cpf, validar_cnpj, validar_telefone
from ..validators.validator import criptografar_senha
from ..services.service import gerar_id
from datetime import datetime
import sqlite3

def cadastrar_usuario(tipo_usuario):
    nome = input("Nome: ")
    if not validar_nome(nome):
        print("Nome inválido! Por favor, tente novamente.")
        return
    
    email = input("Email: ")
    if not validar_email(email):
        print("Email inválido! Por favor, tente novamente.")
        return
    
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone()[0] > 0:
        print("Email já cadastrado!")
        conn.close()
        return
    
    if tipo_usuario == "motorista":
        documento = input("CPF: ")
        if not validar_cpf(documento):
            print("CPF inválido! Por favor, tente novamente.")
            conn.close()
            return
    
    elif tipo_usuario == "empresario":
        documento = input("CNPJ: ")
        if not validar_cnpj(documento):
            print("CNPJ inválido! Por favor, tente novamente.")
            conn.close()
            return
        
    senha = input("Senha: ")
    if not validar_senha(senha):
        print("Senha inválida! Por favor, tente novamente.")
        conn.close()
        return
    
    telefone = input("Telefone: ")
    if not validar_telefone(telefone):
        print("Telefone inválido! Por favor, tente novamente.")
        conn.close()
        return

    id_usuario = gerar_id("usuario")
    data_cadastro = datetime.now().strftime("%Y-%m")

    try:
        cursor.execute("""
            INSERT INTO usuarios (
                id_usuario, nome, tipo_usuario, documento, email, senha, telefone, data_cadastro
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_usuario, nome, tipo_usuario, documento, email, criptografar_senha(senha), telefone, data_cadastro))
        conn.commit()
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Email ou ID já consta no sistema.")
    finally:
        conn.close()

def atualizar_usuario(id_usuario, alteracao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    usuario = cursor.fetchone()
    
    if not usuario:
        print("Usuário não encontrado!")
        conn.close()
        return

    tipo_usuario = usuario["tipo_usuario"]
    nova_info = None

    if alteracao == "nome":
        nova_info = input("Digite o novo nome: ")
        if usuario["nome"] == nova_info:
            print("Escolha um nome diferente do atual")
            conn.close()
            return
        if not validar_nome(nova_info):
            print("Nome inválido! Por favor, tente novamente.")
            conn.close()
            return
        campo = "nome"
    
    elif alteracao == "documento":
        if tipo_usuario == "motorista":
            nova_info = input("CPF: ")
            if usuario["documento"] == nova_info:
                print("Escolha um CPF diferente do atual")
                conn.close()
                return 
            if not validar_cpf(nova_info):
                print("CPF inválido! Por favor, tente novamente.")
                conn.close()
                return
            
        elif tipo_usuario == "empresario":
            nova_info = input("CNPJ: ")
            if usuario["documento"] == nova_info:
                print("Escolha um CNPJ diferente do atual")
                conn.close()
                return
            if not validar_cnpj(nova_info):
                print("CNPJ inválido! Por favor, tente novamente.")
                conn.close()
                return
        campo = "documento"

    elif alteracao == "email":
        nova_info = input("Digite um novo email: ")
        if usuario["email"] == nova_info:
            print("Escolha um email diferente do atual")
            conn.close()
            return
        if not validar_email(nova_info):
            print("Email inválido! Por favor, tente novamente.")
            conn.close()
            return
            
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ? AND id_usuario != ?", (nova_info, id_usuario))
        if cursor.fetchone()[0] > 0:
            print("Email já cadastrado para outro usuário. Por favor, verifique o email e tente novamente.")
            conn.close()
            return
        campo = "email"
    
    elif alteracao == "senha":
        nova_info = input("Digite uma nova senha: ")
        if usuario["senha"] == criptografar_senha(nova_info):
            print("Escolha uma senha diferente da atual")
            conn.close()
            return
        if not validar_senha(nova_info):
            print("Senha inválida! Por favor, tente novamente.")
            conn.close()
            return
        campo = "senha"
    
    elif alteracao == "telefone":
        nova_info = input("Digite um novo telefone: ")
        if usuario["telefone"] == nova_info:
            print("Escolha um telefone diferente do atual")
            conn.close()
            return
        if not validar_telefone(nova_info):
            print("Telefone inválido! Por favor, tente novamente.")
            conn.close()
            return
        campo = "telefone"
    else:
        print("Alteração inválida.")
        conn.close()
        return

    try:
        cursor.execute(f"UPDATE usuarios SET {campo} = ? WHERE id_usuario = ?", (nova_info, id_usuario))
        conn.commit()
        print("Usuário atualizado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro de integridade ao atualizar os dados.")
    finally:
        conn.close()

def visualizar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        print("Usuário não encontrado!")
        return

    print("\n====== PERFIL USUÁRIO ======")
    print('Nome: ', usuario['nome'])
    print('Email: ', usuario['email'])
    print('Tipo de usuário: ', usuario['tipo_usuario'])
    print('Documento: ', usuario['documento'])
    print('Telefone: ', usuario['telefone'])
    print("\n============================")

def deletar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        linhas_afetadas = cursor.rowcount
        conn.commit()
        
        if linhas_afetadas > 0:
            print("Usuário removido com sucesso!")
        else:
            print("Usuário não encontrado!")
    except sqlite3.IntegrityError:
        print("Não é possível remover este usuário pois ele possui unidades ou reservas ativas associadas.")
    finally:
        conn.close()