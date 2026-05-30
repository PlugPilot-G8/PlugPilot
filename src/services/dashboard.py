import matplotlib.pyplot as plt
import numpy as np
from ..managers.database_manager import carregar_database
from datetime import datetime

def dashboard_empresario():
    
    dados = carregar_database()
    usuarios = dados.get("usuarios", {})
    unidades = dados.get("unidades", {})

    fig, ax = plt.subplots(figsize=(10, 6))

    dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    ocupacao = np.random.randint(60, 100, size=7)

    ax.plot(dias, ocupacao, color='#1f77b4',
            marker='o', linewidth=2, markersize=6)
    ax.fill_between(range(len(dias)), ocupacao, alpha=0.3, color='#1f77b4')


    ax.set_title('Uso semanal', fontsize=14, fontweight='bold', pad=20)
    ax.text(0.5, 1.05, 'Taxa de ocupação por dia', transform=ax.transAxes,
            fontsize=10, ha='center', color='gray')

    ax.set_ylabel('Taxa de ocupação por dia', fontsize=10, color='gray')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    ax.legend([f'Seg\nuso : {ocupacao[0]}'], loc='upper left', frameon=True)

    plt.tight_layout()
    plt.show()


def horarios_de_pico():

    dados = carregar_database()
    usuarios = dados.get("usuarios", {})
    unidades = dados.get("unidades", {})

    plt.title('Horários de pico')
    plt.text(0.5, 1.02, 'Reservas por hora', ha='center', va='bottom',
             transform=plt.gca().transAxes, fontsize=10, color='gray')

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
    dados = carregar_database()
    unidades = dados.get("unidades", {})
    carregadores = dados.get("carregadores", {})

    ids_unidades = [
        unidade["id_unidade"]
        for unidade in unidades.values()
        if unidade["id_dono"] == id_usuario
    ]

    total = sum(
        1
        for carregador in carregadores.values()
        if carregador["id_unidade"] in ids_unidades
    )

    return total

def relatorio_carregadores(id_usuario):
    dados = carregar_database()
    unidades = dados.get("unidades", {})
    carregadores = dados.get("carregadores", {})

    ids_unidades = [
        unidade["id_unidade"]
        for unidade in unidades.values()
        if unidade["id_dono"] == id_usuario
    ]

    total = 0
    disponiveis = 0
    ocupados = 0
    offline = 0
    manutencao = 0

    for carregador in carregadores.values():
        if carregador["id_unidade"] in ids_unidades:
            total += 1
            status = carregador["status_atual"].lower()
            if status == "disponivel":
                disponiveis += 1
            elif status == "ocupado":
                ocupados += 1
            elif status == "offline":
                offline += 1
            elif status == "manutencao":
                manutencao += 1

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

def reservas_hoje():
    dados = carregar_database()
    reservas = dados.get("reservas", {})
    hoje = datetime.now().date()
    total = 0

    for reserva in reservas.values():

        data_reserva = datetime.strptime(
            reserva["agendado_para"],
            "%Y-%m-%dT%H:%M:%SZ"
        ).date()

        if data_reserva == hoje:
            total += 1

    return total

def unidades_ativas(id_usuario):
    dados = carregar_database()
    unidades = dados.get("unidades", {})
    total = 0
    for unidade in unidades.values():
        if (
            unidade["id_dono"] == id_usuario
            and unidade.get("status", "").lower() == "ativa"
        ):
            total += 1

    return total 

def receita_estimada_mes(id_usuario):
    dados = carregar_database()
    reservas = dados.get("reservas", {})
    unidades = dados.get("unidades", {})
    total_receita = 0.0

    ids_unidades = [
        unidade["id_unidade"]
        for unidade in unidades.values()
        if unidade["id_dono"] == id_usuario
    ]

    for reserva in reservas.values():
        if reserva["id_unidade"] in ids_unidades:
            total_receita += reserva.get("valor_estimado", 0.0)

    return total_receita       