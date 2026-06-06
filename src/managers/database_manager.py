# database_manager.py - Gerenciamento e inicialização do banco de dados SQLite

import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "database.db")

def conectar():
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL CHECK(tipo_usuario IN ('empresario', 'motorista')),
        documento TEXT,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        telefone TEXT,
        data_cadastro TEXT,
        latitude REAL,
        longitude REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unidades (
        id_unidade TEXT PRIMARY KEY,
        id_dono TEXT NOT NULL,
        status TEXT NOT NULL,
        nome_unidade TEXT NOT NULL,
        endereco_formatado TEXT,
        latitude REAL,
        longitude REAL,
        abertura TEXT,
        fechamento TEXT,
        funciona_fds INTEGER CHECK(funciona_fds IN (0, 1)), -- 0=False, 1=True
        avaliacao_media REAL,
        FOREIGN KEY(id_dono) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carregadores (
        id_carregador TEXT PRIMARY KEY,
        id_unidade TEXT NOT NULL,
        modelo TEXT,
        fabricante TEXT,
        tipo_corrente TEXT CHECK(tipo_corrente IN ('AC', 'DC')),
        potencia_kw REAL,
        tipo_conector TEXT,
        preco_por_kwh REAL,
        status_atual TEXT NOT NULL,
        tipo_monitoramento TEXT CHECK(tipo_monitoramento IN ('hardware', 'manual')),
        id_hardware TEXT,
        ultima_manutencao TEXT,
        permite_reserva INTEGER CHECK(permite_reserva IN (0, 1)),
        fila_virtual INTEGER CHECK(fila_virtual IN (0, 1)),
        plug_and_charge INTEGER CHECK(plug_and_charge IN (0, 1)),
        FOREIGN KEY(id_unidade) REFERENCES unidades(id_unidade) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id_reserva TEXT PRIMARY KEY,
        id_motorista TEXT NOT NULL,
        id_unidade TEXT NOT NULL,
        id_carregador TEXT NOT NULL,
        status_reserva TEXT NOT NULL,
        agendado_para TEXT NOT NULL,
        duracao_minutos INTEGER NOT NULL,
        valor_estimado REAL,
        kwh_consumido REAL,
        FOREIGN KEY(id_motorista) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
        FOREIGN KEY(id_unidade) REFERENCES unidades(id_unidade) ON DELETE RESTRICT,
        FOREIGN KEY(id_carregador) REFERENCES carregadores(id_carregador) ON DELETE RESTRICT
    );
    """)

    conn.commit()
    
    popular_dados_teste(cursor)
    
    conn.commit()
    conn.close()

def popular_dados_teste(cursor):
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        print("[DB] Banco de dados vazio. Injetando logins e dados base de teste...")
        
        cursor.execute("""
            INSERT INTO usuarios (id_usuario, nome, tipo_usuario, documento, email, senha, telefone, data_cadastro)
            VALUES ('51123456', 'Carlos Empresario', 'empresario', '12345678000199', 'empresario@plugpilot.com', 'Admin@123', '11999999999', '2026-06-05')
        """)
        
        cursor.execute("""
            INSERT INTO usuarios (id_usuario, nome, tipo_usuario, documento, email, senha, telefone, data_cadastro, latitude, longitude)
            VALUES ('52123456', 'Lucas Motorista', 'motorista', '12345678900', 'motorista@gmail.com', 'User@123', '11988888888', '2026-06-05', -23.55052, -46.633309)
        """)
        
        cursor.execute("""
            INSERT INTO unidades (id_unidade, id_dono, status, nome_unidade, endereco_formatado, latitude, longitude, abertura, fechamento, funciona_fds, avaliacao_media)
            VALUES ('31123456', '51123456', 'ativa', 'Eletroposto Central', 'Av. Paulista, 1000 - São Paulo, Brazil', -23.561414, -46.655881, '06:00', '22:00', 1, 4.8)
        """)
        
        cursor.execute("""
            INSERT INTO carregadores (id_carregador, id_unidade, modelo, fabricante, tipo_corrente, potencia_kw, tipo_conector, preco_por_kwh, status_atual, tipo_monitoramento, id_hardware, permite_reserva, fila_virtual, plug_and_charge)
            VALUES ('chg_001', '31123456', 'FastCharge v2', 'Volvo', 'DC', 50.0, 'CCS2', 1.99, 'FREE', 'hardware', 'HARDWARE_CHG001', 1, 0, 1)
        """)
        
        print("[DB] Logins e instâncias base criados com sucesso!")