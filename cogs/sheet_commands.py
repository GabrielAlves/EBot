import discord
from discord.ext import commands
from tabulate import tabulate

class SheetCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ler_valor(self, ctx, nome, dia):
        try:
            valor = self.bot.sheet.ler_valor(nome, dia)
            await ctx.send(valor)
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command()
    async def escrever_valor(self, ctx, nome, dia, valor):
        try:
            valor = self.bot.sheet.escrever_valor(nome, dia, valor)
            await ctx.send(valor)
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command()
    async def ler_tabela(self, ctx):
        try:
            header, tabela = self.bot.sheet.ler_tabela()
            tabela = self.bot.tabulacao.tabular(tabela, header)
            await ctx.send(f'```{tabela}```')
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    
    @commands.command()
    async def limpar_tabela(self, ctx, confirmacao = None, valor = 0):
        try:
            if confirmacao == 'confirmar':
                resultado = self.bot.sheet.limpar_tabela(valor)

                if resultado:
                    await ctx.send(f'Tabela limpa com valor {valor}')

                else:
                    await ctx.send(f'Erro ao tenter limpar tabela com valor {valor}')

            else:
                await ctx.send(f'Passe o argumento "confirmar" para confirmar a operação')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command()
    async def gerar_placar(self, ctx):
        try:
            header, placar = self.bot.sheet.gerar_placar()
            tabela = self.bot.tabulacao.tabular(placar, header)
            await ctx.send(f'```{tabela}```')
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command()
    async def farmar_aura(self, ctx):
        try:
            header, primeiro_lugar = self.bot.sheet.farmar_aura()
            tabela = self.bot.tabulacao.tabular(primeiro_lugar, header, num_colunas = 2)
            await ctx.send(f'```{tabela}```')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensgem. tente de novo")

    @commands.command()
    async def preencher_vazios(self, ctx, valor = 0):
        try:
            resultado = self.bot.sheet.preencher_vazios(valor)

            if resultado:
                await ctx.send(f'Vazios preenchidos com {valor}')

            else:
                await ctx.send(f'Erro ao tenter preencher com {valor}')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    @commands.command()
    async def retornar_link(self, ctx):
        try:
            link = self.bot.sheet.retornar_link()
            await ctx.send(link)

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    @commands.command()
    async def abrir_ajuda(self, ctx):
        embed = discord.Embed(
            title="📖 Comandos disponíveis",
            description="Lista de comandos do bot",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="ler_valor <nome> <dia>",
            value=f"Lê o valor da célula correspondente a <nome> e <dia>.\n"
                f"<nome> e <dia> são case-insensitive, mas precisam existir na planilha.\n"
                f"<dia> deve ser escrito sem acentos.\n"
                f"Ex: {self.bot.user.name} ler_valor ezequiel terca",
            inline=False
        )

        embed.add_field(
            name="escrever_valor <nome> <dia> <valor>",
            value=f"Escreve um valor na célula correspondente.\n<dia> deve ser escrito sem acentos.\n<valor> deve ser um número representando o tempo de estudo em minutos.\n"
                f"Ex: {self.bot.user.name} escrever_valor fernando sabado 60",
            inline=False
        )

        embed.add_field(
            name="ler_tabela",
            value=f"Mostra toda a tabela formatada.\n"
                f"Ex: {self.bot.user.name} ler_tabela",
            inline=False
        )

        embed.add_field(
            name="limpar_tabela confirmar [valor]",
            value=f"Limpa toda a tabela preenchendo com um valor (padrão = 0).\n"
                f"É Necessário enviar 'confirmar' junto com o comando para evitar acidentes.\n"
                f"[valor] é opcional. O default de [valor]é 0.\n"
                f"Ex: {self.bot.user.name} limpar_tabela confirmar",
            inline=False
        )

        embed.add_field(
            name="gerar_placar",
            value=f"Gera o ranking com base no tempo total de estudo.\n"
                f"Ex: {self.bot.user.name} gerar_placar",
            inline=False
        )

        embed.add_field(
            name="farmar_aura",
            value=f"Mostra o primeiro lugar do ranking.\n"
                f"Ex: {self.bot.user.name} farmar_aura",
            inline=False
        )

        embed.add_field(
            name="preencher_vazios [valor]",
            value=f"Preenche células vazias com um valor (padrão = 0).\n"
                    f"[valor] é opcional. O default de [valor] é 0.\n"
                f"Ex: {self.bot.user.name} preencher_vazios",
            inline=False
        )

        embed.add_field(
            name="retornar_link",
            value=f"Retorna o link da planilha.\n"
                f"Ex: {self.bot.user.name} retornar_link",
            inline=False
        )

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(SheetCommands(bot))