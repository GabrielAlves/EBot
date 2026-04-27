import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = os.getenv('CHANNEL_ID')

class Bot(commands.Bot):
    def __init__(self, planilha, tabulacao, verificador):
        self.planilha = planilha
        self.tabulacao = tabulacao
        self.verificador = verificador
        self.bot_ligado = False

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = pegar_prefixo, intents = intents)

    async def on_ready(self):
        if not self.bot_ligado:
            self.bot_ligado = True
            print(f'{self.user} ligado!')
            canal = await self.fetch_channel(CHANNEL_ID)
            # await canal.send(f'{self.user} está ligado!\nUse o comando "{self.user.name} ajuda" para ver os comandos disponíveis.')

    async def close(self):
        canal = await self.fetch_channel(CHANNEL_ID)
        # await canal.send(f'{self.user} foi desligado...')


    async def setup_hook(self):
        await self.load_extension('cogs.comandos_planilha')
        await self.load_extension('cogs.comandos_gerais')

def pegar_prefixo(bot, msg):
        nome_bot = bot.user.name if bot.user else "bot"
        return nome_bot + " "