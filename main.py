from planilha import Planilha
from tabulacao import Tabulacao
from bot import Bot
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    print("g1")
    planilha = Planilha()
    print("g2")
    tabulacao = Tabulacao()
    print("g3")
    bot = Bot(planilha, tabulacao)
    print("g4")
    bot.run(DISCORD_TOKEN)
    print("g5")


if __name__ == "__main__":
    main()