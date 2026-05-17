from flask import Flask
from threading import Thread
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)

def configurar_rotas(bot):
    @app.route('/')
    def home():
        return 'Bot está ligado!'

    @app.route('/enviar_msg_desligamento')
    def enviar_msg_desligamento():
        asyncio.run_coroutine_threadsafe(
            bot.close(),
            bot.loop
        )
        return "Mensagem de desligamento enviada"
    
    @app.route('/enviar_placar')
    def enviar_placar():
        asyncio.run_coroutine_threadsafe(
            bot.gerar_placar_para_endpoint(),
            bot.loop
        )

        return "Placar enviado"
        

def run():
    app.run(host = HOST, port = PORT)

def keep_alive():
    thread = Thread(target = run)
    thread.start()