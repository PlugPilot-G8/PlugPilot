# serial_service.py - Leitura serial do Arduino e controle dos carregadores

import time
from datetime import datetime, timedelta

import serial


class SerialService:
    def __init__(
        self,
        porta,
        baud_rate,
        atualizar_status_callback,
        obter_estado_reserva_callback,
    ):
        self.porta = porta
        self.baud_rate = baud_rate
        self.atualizar_status_callback = atualizar_status_callback
        self.obter_estado_reserva_callback = obter_estado_reserva_callback
        self.conexao = None
        self.codigos_ativos = {}

    def conectar(self):
        try:
            self.conexao = serial.Serial(self.porta, self.baud_rate, timeout=1)
            time.sleep(2)
            print(f"Arduino conectado na porta {self.porta}")
        except serial.SerialException as erro:
            print(f"Erro ao conectar na porta {self.porta}: {erro}")
            self.conexao = None

    def normalizar_id_banco(self, id_carregador):
        id_normalizado = id_carregador.strip().lower()

        if "_" not in id_normalizado and id_normalizado.startswith("chg"):
            return f"{id_normalizado[:3]}_{id_normalizado[3:]}"

        return id_normalizado

    def normalizar_id_arduino(self, id_carregador):
        return id_carregador.strip().replace("_", "").upper()

    def normalizar_comando_arduino(self, comando):
        partes = comando.strip().split(":")

        if len(partes) >= 2:
            partes[1] = self.normalizar_id_arduino(partes[1])

        return ":".join(partes)

    def enviar_comando(self, comando):
        if self.conexao is None:
            print("Arduino nao conectado.")
            return

        comando = self.normalizar_comando_arduino(comando)
        self.conexao.write((comando + "\n").encode("utf-8"))

    def escutar(self):
        if self.conexao is None:
            print("Arduino nao conectado.")
            return

        while True:
            linha = self.conexao.readline().decode("utf-8", errors="ignore").strip()

            if linha:
                self.processar_linha(linha)

    def processar_linha(self, linha):
        partes = linha.split(":")

        entidade = partes[0]

        if entidade == "READY":
            self.processar_ready(partes)

        elif entidade == "CODE":
            self.processar_code(partes)

        elif entidade == "LOCKED":
            self.processar_locked(partes)

        elif entidade == "HARDWARE":
            self.processar_hardware(partes)

    def processar_hardware(self, partes):
        if len(partes) != 3:
            return

        _, id_hardware, status_arduino = partes
        self.atualizar_status_callback(id_hardware, status_arduino)

    def processar_ready(self, partes):
        if len(partes) != 2:
            return

        _, id_carregador = partes
        id_carregador = self.normalizar_id_banco(id_carregador)

        comando_estado = self.obter_estado_reserva_callback(id_carregador)
        status = comando_estado.split(":", 1)[0]
        self.atualizar_status_callback(id_carregador, status)
        self.enviar_comando(comando_estado)

    def processar_code(self, partes):
        if len(partes) != 3:
            return

        _, id_carregador, codigo = partes
        id_carregador = self.normalizar_id_banco(id_carregador)

        self.codigos_ativos[id_carregador] = {
            "codigo": codigo,
            "gerado_em": datetime.now(),
            "expira_em": datetime.now() + timedelta(seconds=60),
        }

    def processar_locked(self, partes):
        if len(partes) != 2:
            return

        _, id_carregador = partes
        id_carregador = self.normalizar_id_banco(id_carregador)

        comando_estado = self.obter_estado_reserva_callback(id_carregador)
        status = comando_estado.split(":", 1)[0]
        self.atualizar_status_callback(id_carregador, status)

    def liberar_por_codigo(
        self,
        id_carregador,
        id_motorista,
        codigo_digitado,
        validar_liberacao_callback,
    ):
        permitido, motivo = validar_liberacao_callback(
            id_carregador,
            id_motorista,
            codigo_digitado,
            self.codigos_ativos,
        )

        print(motivo)

        if permitido:
            self.enviar_comando(f"ALLOW:{id_carregador}")
        else:
            self.enviar_comando(f"DENY:{id_carregador}")

        return permitido
