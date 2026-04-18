from sheet import Sheet
from bot import Bot
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    sheet = Sheet()
    bot = Bot(sheet)
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()