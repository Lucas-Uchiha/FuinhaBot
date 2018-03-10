import discord
import random
from Utilities.Log import Log
from Utilities.Time import Time
from Utilities.Files import File
from Utilities.ImageFormats import ImageFormats
from Utilities.Functions import get_file_name, get_file_extension, is_url, is_string_formated, is_position
from Componentes.Usuario import Usuario
from Web.FileDownloader import FileDownloader
from Image.ImageHandler import ImageHandler
from Exceptions.Exceptions import ArgumentsOutOfFormat, FileAlreadyExists


class Fuinha(discord.Client):
    def __init__(self, base=".", tempomin=10):
        super().__init__()
        self.log = Log()
        self.base = base
        self.tempoMin = tempomin
        self.meme_list = File.get_all_files()
        self.comandos = {
            self.base + "help": self._help,
            self.base + "stats": self._estatisticas,
            self.base + "makememe": self._makememe,
            self.base + "getmeme": self._getmeme,
            self.base + "randmeme": self._randmeme
        }

    # Sobrescreve evento da classe Client
    async def on_ready(self):
        self.log.salva("========================================")
        self.log.salva("Iníciando FuinhaBot!")
        self.log.salva("Versão do discord.py: " + discord.__version__)
        self.log.salva("Logado como: {0}".format(self.user))
        self.log.salva("========================================")

    # Sobrescreve evento da classe Client
    async def on_message(self, message):
        # Ignora mensagens do proprio bot
        if message.author == self.user:
            return

        # Caso a mensagem seja um comando
        if self._msg_startswith(message, "") and len(message.content) > 4:
            # Checa se o usuario digitou o comando a menos de 10 segundos
            try:
                tenpo_relativo = Time.agora() - Usuario.get_last_use(message.author)
            except KeyError:
                tenpo_relativo = 100
                Usuario.add(message.author)

            if tenpo_relativo >= 10:
                # Caso o comando seja um comando publico
                try:
                    comando = self._get_comando_e_args(message)
                    Usuario.update(message.author)  # Atualiza o momento do ultimo comando utilizado
                    await self.comandos[comando["cmd"]](message)
                except KeyError:
                    Usuario.reset(message.author)
                    self._comando_inexistente()
                except ArgumentsOutOfFormat:
                    self.log.salva("O comando acima foi invocado com parametros incorretos.")

    '#--------------------- Comandos publicos ---------------------#'

    async def _help(self, message):
        msg = ("Olá {0.author.mention}, o maluco que me programou ta com preguiça de escrever isso direito."
            " Faz ele me terminar logo. =/".format(message))

        self.log.salva("Comando help invocado por: " + str(message.author))
        await self.send_message(message.channel, msg)

    async def _estatisticas(self,message):
        msg = "Olá {0.author.mention}, no futuro eu poderei responder a esse comando.".format(message)
        self.log.salva("Comando estatisticas invocado por: " + str(message.author))
        await self.send_message(message.channel, msg)

    async def _makememe(self, message):
        args = self._get_comando_e_args(message)["args"]

        if message.channel.is_private:
            self.log.salva("Comando makememe invocado por: " + str(message.author))

            if self._check_format(args):
                FileDownloader.download(args[0])
                file = get_file_name(args[0])
                # makememe url nomedomeme posicaotexto "texto"

                try:
                    ImageHandler.draw_in_image(file, args[1], args[2].upper(), args[3])

                    msg = "Meme gerado com sucesso! Para usá-lo digite: " + self.base + "getmeme " + args[1]

                    new = args[1] + "." + get_file_extension(file)
                    self.meme_list.append(new) # Insert new meme in list
                except FileAlreadyExists:
                    msg = "Já existe um meme com esse nome, tenta outro ae campeão."
                    Usuario.reset(message.author)

                await self.send_message(message.channel, msg)
            else:
                raise ArgumentsOutOfFormat
        else:
            Usuario.reset(message.author)

    async def _getmeme(self, message):
        args = self._get_comando_e_args(message)["args"]
        self.log.salva("Comando getmeme invocado por: " + str(message.author))

        if len(args) >= 1 and is_string_formated(args[0], 1, 20):
            result = self._search_meme(args[0])
            if isinstance(result, str):
                file = "./Memes/" + result
                await self.send_file(message.channel, file)
            else:
                msg = "Esse meme ainda não existe. =/"
                await self.send_message(message.channel, msg)
        else:
            raise ArgumentsOutOfFormat

    async def _randmeme(self, message):
        self.log.salva("Comando randmeme invocado por: " + str(message.author))
        n = random.randint(0, len(self.meme_list) - 1)
        file = "./Memes/" + self.meme_list[n]
        await self.send_file(message.channel, file)

    '#--------------------- Metodos privados da classe ---------------------#'

    # Analisa se mensagem é um comando
    def _msg_startswith(self, msg, cmd):
        return msg.content.startswith(self.base + cmd)

    # retorna um dicionario contento o comando e a lista de parametros caso exista
    def _get_comando_e_args(self,msg):
        text = msg.content.split("\"")
        lista = text[0].split(" ")

        if len(lista) == 5:
            lista[4] = text[-2]

        re = {
            "cmd": lista[0],
            "args": lista[1:]
        }

        return re

    def _check_format(self, args):
        if len(args) == 4:
            url = is_url(args[0])
            name = is_string_formated(args[1], 1, 20)
            pos = is_position(args[2])
            text = is_string_formated(args[3])

            return url == name == pos == text
        else:
            raise ArgumentsOutOfFormat

    def _comando_inexistente(self):
        self.log.salva("Comando inválido utilizado.")

    def _search_meme(self,name):
        formats = [f.name.lower() for f in ImageFormats]

        for m in self.meme_list:
            for f in formats:
                if m == name + "." + f:
                    return m

        return False
