from Main.Fuinha import Fuinha
from Utilities.Files import File

dados = File.loadConfig()

bot = Fuinha(base="$$")
bot.run(dados["token"])
