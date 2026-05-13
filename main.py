from planilha import Planilha
from tabulacao import Tabulacao
from bot import Bot
from verificador import Verificador
from dotenv import load_dotenv
import os
from keep_alive import keep_alive

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    keep_alive()
    planilha = Planilha()
    tabulacao = Tabulacao()
    verificador = Verificador(planilha)
    bot = Bot(planilha, tabulacao, verificador)
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()