from discord.ext import commands
from excecoes import *

abreviacoes_dias = {
    "dom" : "domingo",
    "seg" : "segunda",
    "ter" : "terca",
    "qua" : "quarta",
    "qui" : "quinta",
    "sex" : "sexta",
    "sab" : "sabado"
}

class ComandosPlanilha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="escrever", aliases=["escrever_valor"])
    async def escrever_valor(self, ctx, nome, dia, valor):
        try:
            if len(dia) == 3: dia = abreviacoes_dias[dia]
            header, tabela = self.bot.planilha.escrever_valor(nome, dia, valor)
            tabela = self.bot.tabulacao.tabular(tabela, header)
            await ctx.send(f'```{tabela}```')
        
        except (NomeInvalidoErro, DiaInvalidoErro, ValorInvalidoErro) as e:
            await ctx.send(e)

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    @commands.command(name="somar", aliases=["somar_valor"])
    async def somar_valor(self, ctx, nome, dia, valor):
        try:
            if len(dia) == 3: dia = abreviacoes_dias[dia]
            header, tabela = self.bot.planilha.somar_valor(nome, dia, valor)
            tabela = self.bot.tabulacao.tabular(tabela, header)
            await ctx.send(f'```{tabela}```')

        except (NomeInvalidoErro, DiaInvalidoErro, ValorInvalidoErro) as e:
            await ctx.send(e)
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command(name="tabela", aliases=["ler_tabela"])
    async def ler_tabela(self, ctx):
        try:
            header, tabela = self.bot.planilha.ler_tabela()
            tabela = self.bot.tabulacao.tabular(tabela, header)
            await ctx.send(f'```{tabela}```')
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    
    @commands.command(name="zerar", aliases=["zerar_tabela"])
    async def zerar_tabela(self, ctx, confirmacao = None, valor = 0):
        try:
            if confirmacao == 'confirmar':
                resultado = self.bot.planilha.zerar_tabela(0)

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
            header, placar = self.bot.planilha.gerar_placar()
            tabela = self.bot.tabulacao.tabular(placar, header)
            await ctx.send(f'```{tabela}```')
            await ctx.send(f"Obs: se esse for o placar final da semana, não se esqueça de zerar a tabela com o comando '{self.bot.get_command("zerar_tabela")}'.")
        
        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")
    
    @commands.command(name="top", aliases=["farmar_aura"])
    async def farmar_aura(self, ctx):
        try:
            header, primeiro_lugar = self.bot.planilha.farmar_aura()
            tabela = self.bot.tabulacao.tabular(primeiro_lugar, header, num_colunas = 2)
            await ctx.send(f'```{tabela}```')

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensgem. tente de novo")

    @commands.command(name="link", aliases=["retornar_link"])
    async def retornar_link(self, ctx):
        try:
            link = self.bot.planilha.retornar_link()
            await ctx.send(link)

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensagem. tente de novo")

    @commands.command(name="linha", aliases=["ler_linha"])
    async def ler_linha(self, ctx, nome):
        try:
            header, linha = self.bot.planilha.ler_linha(nome)
            tabela = self.bot.tabulacao.tabular(linha, header)
            await ctx.send(f'```{tabela}```')

        except (NomeInvalidoErro) as e:
            await ctx.send(e)

        except Exception as e:
            print(e)
            await ctx.send("Erro ao enviar mensgem. tente de novo")

    
async def setup(bot):
    await bot.add_cog(ComandosPlanilha(bot))