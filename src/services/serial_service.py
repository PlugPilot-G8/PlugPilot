# serial_service.py - Leitura da comunicacao serial do Arduino e atualizacao dos carregadores

import time
import serial

class SerialService:
    def __init__(self, porta, baud_rate, atualizar_status_callback):
        self.porta = porta
        self.baud_rate = baud_rate
        self.atualizar_status_callback = atualizar_status_callback
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = serial.Serial(self.porta, self.baud_rate, timeout=1)
            time.sleep(2)
            print(f"Arduino conectado na porta {self.porta}")
        except serial.SerialException as erro:
            print(f"Erro ao conectar na porta {self.porta}: {erro}")
            self.conexao = None

    def escutar(self):
        if self.conexao is None:
            print("Arduino nao conectado.")
            return

        print("Monitorando Arduino...")

        while True:
            linha = self.conexao.readline().decode("utf-8").strip()

            if linha:
                print(f"Recebido: {linha}")
                self.processar_linha(linha)

    def processar_linha(self, linha):
        partes = linha.split(":")

        if len(partes) != 3:
            return

        entidade, id_hardware, status = partes

        if entidade != "HARDWARE":
            return

        self.atualizar_status_callback(id_hardware, status)
