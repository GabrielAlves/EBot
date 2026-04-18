import discord
from discord.ext import commands
from utils import get_prefix
from tabulacao import Tabulacao

class Bot(commands.Bot):
    def __init__(self, sheet):
        self.sheet = sheet
        self.tabulacao = Tabulacao()

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = get_prefix, intents = intents)

    async def on_ready(self):
        print(f'{self.user} ligado!')

    async def setup_hook(self):
        await self.load_extension('cogs.sheet_commands')