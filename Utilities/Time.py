# Gerencia informações de data e hora
from datetime import datetime


class Time:
    @staticmethod
    def agora():
        return datetime.timestamp(datetime.now())

    @staticmethod
    def dia():
        return datetime.now().strftime("%d")

    @staticmethod
    def mes():
        return datetime.now().strftime("%m")

    @staticmethod
    def ano():
        return datetime.now().strftime("%Y")

    @staticmethod
    def dataFormatada():
        return datetime.now().strftime("%d-%m-%Y")

    @staticmethod
    def horaFormatada():
        return datetime.now().strftime("%H:%M:%S")
