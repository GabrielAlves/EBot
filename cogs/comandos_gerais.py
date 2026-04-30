import discord
from discord.ext import commands
from excecoes import *
import re

class ComandosGerais(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sobre", aliases=["abrir_sobre"])
    async def abrir_sobre(self, ctx):
        embed = discord.Embed(
            title="Sobre o Bot",
            description=f"Este bot acessa e altera a planilha presente em {self.bot.planilha.retornar_link()}.\n"
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

    @commands.command(name="em_minutos", aliases=["converter_para_minutos"])
    async def converter_para_minutos(self, ctx, valor):
        try:
            padrao = r'(\d+)h(\d+)m'
            match = re.match(padrao, valor)
            minutos = int(match.group(1)) * 60 + int(match.group(2))
            await ctx.send(minutos)

        except Exception as e:
            print(e)
            await ctx.send(f"Erro:{e}")

    @commands.command(name="em_horas", aliases=["converter_para_horas"])
    async def converter_para_horas(self, ctx, valor):
        self.bot.verificador.verificar_valor(valor)
        valor = int(valor)

        try:
            horas = valor // 60
            minutos = valor % 60
            await ctx.send(f"{horas}h{minutos}m")

        except ValorInvalidoErro as e:
            await ctx.send(e)

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensgem. tente de novo")

    @commands.command(name="ajuda", aliases=["abrir_ajuda"])
    async def abrir_ajuda(self, ctx):
        embed = discord.Embed(
            title="Comandos do Bot",
            description=f"Todos os comandos devem ser precedidos por '{self.bot.user.name} '.",
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
                "escrever", "<nome> <dia> <valor>",
                "Escreve um valor na célula correspondente.\n"
                "<nome> deve existir na planilha.\n"
                "<valor> deve ser um número representando minutos."
                "Argumentos válidos para <dia> : domingo, segunda, terca, quarta, quinta, sexta, sabado.\n"
                "Abreviações válidas para <dia> : dom, seg, ter, qua, qui, sex, sab.",
                "escrever fernando sabado 60", "✏️"
            ),

            formatar_cmd(
                "somar", "<nome> <dia> <valor>",
                "Soma <valor> no valor atual presente na célula correspondente.\n"
                "<nome> deve existir na planilha.\n"
                "Argumentos válidos para <dia> : domingo, segunda, terca, quarta, quinta, sexta, sabado.\n"
                "Abreviações válidas para <dia> : dom, seg, ter, qua, qui, sex, sab.",
                "somar nery segunda 30", "➕"
            ),

            formatar_cmd(
                "tabela", "",
                "Mostra toda a tabela formatada.\n"
                "Se a visualização da tabela estiver bagunçada. Tente reduzir o zoom da tela pra ver melhor",
                "tabela", "📋"
            ),

            formatar_cmd(
                "zerar", "",
                "Zera toda a tabela (define todos os tempos como 0).\n"
                "Este comando não a zera de fato, mas aponta o usuário para outro comando para que ele não zere a tabela acidentalmente com esse comando.",
                "zerar", "⚠️"
            ),

            formatar_cmd(
                "placar", "",
                "Gera o ranking com base no tempo total de estudo.",
                "placar", "📊"
            ),

            formatar_cmd(
                "top", "",
                "Mostra o primeiro lugar do ranking.",
                "top", "🥇"
            ),

            formatar_cmd(
                "linha", "<nome>",
                "Mostra a linha completa de um usuário.",
                "linha carlos", "👤"
            ),

            formatar_cmd(
                "em_minutos", "<tempo_horas>",
                "Converte um tempo em formato de horas para minutos.\n",
                "em_minutos 2h0m", "🕒➡️⏱️"
            ),

            formatar_cmd(
                "em_horas", "<tempo_minutos>",
                "Converte um tempo em minutos para formato de horas.\n",
                "em_horas 100", "⏱️➡️🕒"
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

async def setup(bot):
    await bot.add_cog(ComandosGerais(bot))