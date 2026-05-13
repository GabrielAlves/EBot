from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# Transforma o projeto em uma aplicação web para que possa ser pingado e não cair por inatividade

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot está ligado!'

def run():
    app.run(host = HOST, port = PORT)

def keep_alive():
    thread = Thread(target = run)
    thread.start()