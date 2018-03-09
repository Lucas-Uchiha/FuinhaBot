# Responsavel por controlar o acesso de usuarios ao bot
from Utilities.Time import Time


class Usuario:
    _users = {}

    @staticmethod
    def add(usuario):
        Usuario._users[usuario] = 0

    @staticmethod
    def remove(usuario):
        Usuario._users.pop(usuario)

    @staticmethod
    def update(usuario):
        Usuario._users[usuario] = Time.agora()

    @staticmethod
    def reset(usuario):
        Usuario._users[usuario] = 0

    @staticmethod
    def get_last_use(usuario):
        return Usuario._users[usuario]
