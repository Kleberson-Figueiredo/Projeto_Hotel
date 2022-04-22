from distutils.command.config import config
import json

with open('credenciais.json') as arquivo_json:
    config = json.load(arquivo_json)

USER =  config.get("USER")
PASSWORD = config.get("PASSWORD")
HOST = config.get("HOST")
PORT = config.get("PORT")
DATABASE = config.get("DATABASE")
JWT_SECRET_KEY = config.get("JWT_SECRET_KEY")
