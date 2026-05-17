from planilha import Planilha
from tabulacao import Tabulacao
from bot import Bot
from verificador import Verificador
from dotenv import load_dotenv
import os
from web_app import keep_alive, configurar_rotas

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    planilha = Planilha()
    tabulacao = Tabulacao()
    verificador = Verificador(planilha)
    bot = Bot(planilha, tabulacao, verificador)
    
    configurar_rotas(bot)
    keep_alive()

    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()