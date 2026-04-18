import discord
from discord.ext import commands
from tabulate import tabulate

class SheetCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ler", aliases = ["ler_valor"])
    async def ler_valor(self, ctx, nome, dia):
        try:
            valor = self.bot.sheet.ler_valor(nome, dia)
            await ctx.send(valor)
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command(name="escrever", aliases=["escrever_valor"])
    async def escrever_valor(self, ctx, nome, dia, valor):
        try:
            header, tabela = self.bot.sheet.escrever_valor(nome, dia, valor)
            tabela = self.bot.tabulacao.tabular(tabela, header)
            await ctx.send(f'```{tabela}```')
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command(name="tabela", aliases=["ler_tabela"])
    async def ler_tabela(self, ctx):
        try:
            header, tabela = self.bot.sheet.ler_tabela()
            tabela = self.bot.tabulacao.tabular(tabela, header)
            await ctx.send(f'```{tabela}```')
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    
    @commands.command(name="zerar", aliases=["zerar_tabela"])
    async def zerar_tabela(self, ctx, confirmacao = None, valor = 0):
        try:
            if confirmacao == 'confirmar':
                resultado = self.bot.sheet.zerar_tabela(0)

                if resultado:
                    await ctx.send(f'Tabela zerada com sucesso')

                else:
                    await ctx.send(f'Erro ao tenter zerar tabela')

            else:
                await ctx.send(f'Passe o argumento "confirmar" para confirmar a operação')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command(name="placar", aliases=["gerar_placar"])
    async def gerar_placar(self, ctx):
        try:
            header, placar = self.bot.sheet.gerar_placar()
            tabela = self.bot.tabulacao.tabular(placar, header)
            await ctx.send(f'```{tabela}```')
            await ctx.send(f"Obs: se esse for o placar final da semana, não se esqueça de zerar a tabela com o comando '{self.bot.get_command("zerar_tabela")}'.")
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command(name="top", aliases=["farmar_aura"])
    async def farmar_aura(self, ctx):
        try:
            header, primeiro_lugar = self.bot.sheet.farmar_aura()
            tabela = self.bot.tabulacao.tabular(primeiro_lugar, header, num_colunas = 2)
            await ctx.send(f'```{tabela}```')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensgem. tente de novo")

    @commands.command(name="completar", aliases=["completar_vazios"])
    async def completar_zeros(self, ctx):
        try:
            resultado = self.bot.sheet.completar_zeros(0)

            if resultado:
                await ctx.send(f'Vazios preenchidos com 0')

            else:
                await ctx.send(f'Erro ao tenter preencher com 0')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    @commands.command(name="link", aliases=["retornar_link"])
    async def retornar_link(self, ctx):
        try:
            link = self.bot.sheet.retornar_link()
            await ctx.send(link)

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    @commands.command(name="linha", aliases=["ler_linha"])
    async def ler_linha(self, ctx, nome):
        try:
            header, linha = self.bot.sheet.ler_linha(nome)
            tabela = self.bot.tabulacao.tabular(linha, header)
            await ctx.send(f'```{tabela}```')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensgem. tente de novo")

    @commands.command(name="ajuda", aliases=["abrir_ajuda"])
    async def abrir_ajuda(self, ctx):
        embed = discord.Embed(
            title="Comandos do Bot",
            description=f"Todos os comandos devem ser precedidos por '{self.bot.user.name} '",
            color=discord.Color.blue()
        )

        def formatar_cmd(nome, uso, descricao, exemplo, emoji):
            cmd = self.bot.get_command(nome)
            aliases = ", ".join(cmd.aliases) if cmd.aliases else "Nenhum"

            return (
                f"{emoji} **{cmd.name} {uso}**\n"
                f"{descricao}\n"
                f"**Aliases:** `{aliases}`\n"
                f"**Exemplo:** `{self.bot.user.name} {exemplo}`"
            )

        comandos = [
            formatar_cmd(
                "ler", "<nome> <dia>",
                "Lê o valor da célula correspondente a <nome> e <dia>.\n"
                "<nome> e <dia> são case-insensitive.\n"
                "<dia> deve ser escrito sem acentos.",
                "ler ezequiel terca", "📖"
            ),

            formatar_cmd(
                "escrever", "<nome> <dia> <valor>",
                "Escreve um valor na célula correspondente.\n"
                "<dia> deve ser escrito sem acentos.\n"
                "<valor> deve ser um número representando minutos.",
                "escrever fernando sabado 60", "✏️"
            ),

            formatar_cmd(
                "tabela", "",
                "Mostra toda a tabela formatada.\n"
                "Se a visualização da tabela estiver bagunçada. Tente reduzir o zoom da tela pra ver melhor",
                "tabela", "📊"
            ),

            formatar_cmd(
                "zerar", "confirmar",
                "Zera toda a tabela (define todos os tempos como 0).\n"
                "Necessário usar 'confirmar' para evitar acidentes.",
                "zerar confirmar", "⚠️"
            ),

            formatar_cmd(
                "placar", "",
                "Gera o ranking com base no tempo total de estudo.",
                "placar", "🏆"
            ),

            formatar_cmd(
                "top", "",
                "Mostra o primeiro lugar do ranking.",
                "top", "🥇"
            ),

            formatar_cmd(
                "completar", "",
                "Preenche células vazias com 0.",
                "completar", "🧩"
            ),

            formatar_cmd(
                "linha", "<nome>",
                "Mostra a linha completa de um usuário.",
                "linha carlos", "👤"
            ),

            formatar_cmd(
                "link", "",
                "Retorna o link da planilha.",
                "link", "🔗"
            ),

            formatar_cmd(
                "sobre", "",
                "Abre o sobre (o bot).",
                "sobre", "ℹ️"
            ),
        ]

        for cmd in comandos:
            embed.add_field(
                name="\u200b",
                value=cmd,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="sobre", aliases=["abrir_sobre"])
    async def abrir_sobre(self, ctx):
        embed = discord.Embed(
            title="Sobre o Bot",
            description=f"Este bot acessa e altera a planilha presente em {self.bot.sheet.retornar_link()}.\n"
            f"Para ver todos os comandos disponíveis, use o comando '{self.bot.get_command("abrir_ajuda")}'\n",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Programador",
            value="Gabriel Alves",
            inline=False
        )

        embed.add_field(
            name="Repositório",
            value="https://github.com/GabrielAlves/EstudoBot",
            inline=False
        )

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(SheetCommands(bot))