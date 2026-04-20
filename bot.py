import discord
from discord.ext import commands
from utils import get_prefix
from tabulacao import Tabulacao
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = os.getenv('CHANNEL_ID')

class Bot(commands.Bot):
    def __init__(self, sheet):
        self.sheet = sheet
        self.tabulacao = Tabulacao()
        self.bot_is_on = False

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = get_prefix, intents = intents)

    async def on_ready(self):
        if not self.bot_is_on:
            self.bot_is_on = True
            print(f'{self.user} ligado!')
            channel = await self.fetch_channel(CHANNEL_ID)
            await channel.send(f'{self.user} está ligado!\nUse o comando "{self.user.name} ajuda" para ver os comandos disponíveis.')

    async def close(self):
        channel = await self.fetch_channel(CHANNEL_ID)
        await channel.send(f'{self.user.name} foi desligado...')

    async def on_disconnect(self):
        print(f"{self.user.name} desconectou do Discord.")


    async def setup_hook(self):
        await self.load_extension('cogs.sheet_commands')