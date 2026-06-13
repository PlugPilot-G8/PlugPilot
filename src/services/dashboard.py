# dashboard_service.py - Relatórios e gráficos estatísticos via SQLite

import matplotlib.pyplot as plt
import numpy as np
from ..managers.database_manager import conectar
from datetime import datetime

def dashboard_empresario(id_usuario):
    fig, ax = plt.subplots(figsize=(10, 6))

    dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    ocupacao = np.random.randint(60, 100, size=7)

    ax.plot(dias, ocupacao, color='#1f77b4', marker='o', linewidth=2, markersize=6)
    ax.fill_between(range(len(dias)), ocupacao, alpha=0.3, color='#1f77b4')

    ax.set_title('Uso semanal', fontsize=14, fontweight='bold', pad=20)
    ax.text(0.5, 1.05, 'Taxa de ocupação por dia', transform=ax.transAxes, fontsize=10, ha='center', color='gray')
    ax.set_ylabel('Taxa de ocupação por dia', fontsize=10, color='gray')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    ax.legend([f'Seg\nuso : {ocupacao[0]}'], loc='upper left', frameon=True)

    plt.tight_layout()
    plt.show()

def horarios_de_pico(id_usuario):
    plt.title('Horários de pico')
    plt.text(0.5, 1.02, 'Reservas por hora', ha='center', va='bottom', transform=plt.gca().transAxes, fontsize=10, color='gray')

    horarios = ['06', '08', '10', '12', '14', '16', '18', '20', '22']
    taxa_de_ocupacao = [10, 35, 55, 70, 65, 85, 90, 70, 30]

    plt.style.use('_mpl-gallery')
    plt.bar(horarios, taxa_de_ocupacao, color='#4472C4', edgecolor='none')
    plt.xlabel('Horários do Dia')
    plt.ylabel('Reservas por hora')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

def total_carregadores(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(c.id_carregador) FROM carregadores c
        JOIN unidades u ON c.id_unidade = u.id_unidade
        WHERE u.id_dono = ?
    """, (id_usuario,))
    
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0


def relatorio_carregadores(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(c.id_carregador) as total,
            SUM(CASE WHEN UPPER(c.status_atual) IN ('FREE', 'DISPONIVEL') THEN 1 ELSE 0 END) as disponiveis,
            SUM(CASE WHEN UPPER(c.status_atual) IN ('IN_USE', 'OCUPADO') THEN 1 ELSE 0 END) as ocupados,
            SUM(CASE WHEN LOWER(c.status_atual) = 'offline' THEN 1 ELSE 0 END) as offline,
            SUM(CASE WHEN LOWER(c.status_atual) = 'manutencao' THEN 1 ELSE 0 END) as manutencao
        FROM carregadores c
        JOIN unidades u ON c.id_unidade = u.id_unidade
        WHERE u.id_dono = ?
    """, (id_usuario,))
    
    resultado = cursor.fetchone()
    conn.close()

    total = resultado["total"] if resultado["total"] else 0
    disponiveis = resultado["disponiveis"] if resultado["disponiveis"] else 0
    ocupados = resultado["ocupados"] if resultado["ocupados"] else 0
    offline = resultado["offline"] if resultado["offline"] else 0
    manutencao = resultado["manutencao"] if resultado["manutencao"] else 0

    print(f"Total de carregadores: {total}")
    print(f"Disponíveis: {disponiveis}")
    print(f"Ocupados: {ocupados}")
    print(f"Offline: {offline}")
    print(f"Em manutenção: {manutencao}")

    return {
        "total": total,
        "disponiveis": disponiveis,
        "ocupados": ocupados,
        "offline": offline,
        "manutencao": manutencao
    }

def reservas_hoje(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(r.id_reserva) FROM reservas r
        JOIN unidades u ON r.id_unidade = u.id_unidade
        WHERE u.id_dono = ? AND date(r.agendado_para) = date('now', 'localtime')
    """, (id_usuario,))
    
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def unidades_ativas(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) FROM unidades 
        WHERE id_dono = ? AND LOWER(status) = 'ativa'
    """, (id_usuario,))
    
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def receita_estimada_mes(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(r.valor_estimado) FROM reservas r
        JOIN unidades u ON r.id_unidade = u.id_unidade
        WHERE u.id_dono = ?
    """, (id_usuario,))
    
    total_receita = cursor.fetchone()[0]
    conn.close()
    return total_receita if total_receita else 0.0
