# Gerencia os Logs do sistema
from Utilities.Time import Time


class Log:
    def __init__(self):
        self.mensagem = ""

    def salva(self,msg):
        self.mensagem = msg
        log = self._gera()
        self._escreveTerminal(log)
        self._escreveArquivo(log)

    def _gera(self):
        return "* " + Time.horaFormatada() + " - " + self.mensagem

    def _escreveTerminal(self,msg):
        print(msg)

    def _escreveArquivo(self,msg):
        file = open("../Logs/" + Time.dataFormatada() + ".txt","a")
        file.write(msg + "\n")
        file.close()
