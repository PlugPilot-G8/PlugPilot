import sqlite3
import os

# Definindo o diretório e o caminho do banco de dados
db_dir = "src/data"
db_path = os.path.join(db_dir, "database.db")

# Garantir que a pasta exista
os.makedirs(db_dir, exist_ok=True)

# Conectar ao banco de dados (isso cria o arquivo se não existir)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ativar suporte a Chaves Estrangeiras no SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Tabela de Usuários
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

# 2. Tabela de Unidades (Eletropostos)
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

# 3. Tabela de Carregadores
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

# 4. Tabela de Reservas
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

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print(f"Banco de dados criado com sucesso em: {db_path}")