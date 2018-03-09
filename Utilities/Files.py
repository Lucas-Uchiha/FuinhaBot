import json
from os import listdir
from os.path import isfile, join


class File:
    _memes_path = "../Memes/"

    @staticmethod
    def loadConfig():
        try:
            return json.load(open("../config.json", "r"))
        except FileNotFoundError:
            print("O arquivo config.json não foi encontrado.")
            exit(1)

    @staticmethod
    def get_all_files():
        files = [f for f in listdir(File._memes_path) if isfile(join(File._memes_path, f))]
        return files
