from discord.ext import commands
from excecoes import *

class ComandosPlanilha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="escrever", aliases=["escrever_valor"])
    async def escrever_valor(self, ctx, nome, dia, valor):
        try:
            self.bot.verificador.verificar_valor(valor)
            
            if len(dia) == 3: dia = self.bot.verificador.verificar_abreviacao(dia)
            else: self.bot.verificador.verificar_dia(dia)

            linha = self.bot.verificador.converter_nome_em_linha(nome)
            coluna = self.bot.verificador.converter_dia_em_coluna(dia)
            header, linha = self.bot.planilha.escrever_valor(linha, coluna, valor)
            linha = self.bot.tabulacao.tabular(header, linha)
            await ctx.send(f'```{linha}```')
        
        except (NomeInvalidoErro, DiaInvalidoErro, AbreviacaoInvalidaErro, ValorInvalidoErro) as e:
            await ctx.send(e)

        except Exception as e:
            await ctx.send(f"Erro: {e}")

    @commands.command(name="somar", aliases=["somar_valor"])
    async def somar_valor(self, ctx, nome, dia, valor):
        try:
            self.bot.verificador.verificar_valor(valor)

            if len(dia) == 3: dia = self.bot.verificador.verificar_abreviacao(dia)
            else: self.bot.verificador.verificar_dia(dia)

            linha = self.bot.verificador.converter_nome_em_linha(nome)
            coluna = self.bot.verificador.converter_dia_em_coluna(dia)
            header, linha = self.bot.planilha.somar_valor(linha, coluna, valor)
            linha = self.bot.tabulacao.tabular(header, linha)
            await ctx.send(f'```{linha}```')

        except (NomeInvalidoErro, DiaInvalidoErro, AbreviacaoInvalidaErro, ValorInvalidoErro) as e:
            await ctx.send(e)
        
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="tabela", aliases=["ler_tabela"])
    async def ler_tabela(self, ctx):
        try:
            header, tabela = self.bot.planilha.ler_tabela()
            tabela = self.bot.tabulacao.tabular(header, tabela)
            await ctx.send(f'```{tabela}```')
        
        except Exception as e:
            await ctx.send(f"Erro: {e}")

    
    @commands.command(name="zerar", aliases=["preencher_zeros"])
    async def zerar_tabela(self, ctx):
        try:
            await ctx.send(f"Tem certeza que deseja zerar a tabela? Digite `{self.bot.user.name} confirmar_zerar` para continuar.")

        except Exception as e:
            await ctx.send(f"Erro: {e}")

    @commands.command(name="confirmar_zerar", aliases=["zerar_tabela"])
    async def confirmar_zerar(self, ctx):
        try:
            header, tabela = self.bot.planilha.ler_tabela()
            tabela = self.bot.tabulacao.tabular(header, tabela)
            await ctx.send(f'```{tabela}```')

        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="placar", aliases=["gerar_placar"])
    async def gerar_placar(self, ctx):
        try:
            header, placar = self.bot.planilha.gerar_placar()
            tabela = self.bot.tabulacao.tabular(header, placar)
            await ctx.send(f'```{tabela}```')
            await ctx.send(f"Obs: se esse for o placar final da semana, não se esqueça de zerar a tabela com o comando '{self.bot.get_command("zerar_tabela")}'.")
        
        except Exception as e:
            await ctx.send(f"Erro: {e}")
    
    @commands.command(name="top", aliases=["farmar_aura"])
    async def farmar_aura(self, ctx):
        try:
            header, primeiro_lugar = self.bot.planilha.farmar_aura()
            tabela = self.bot.tabulacao.tabular(header, primeiro_lugar, num_colunas = 2)
            await ctx.send(f'```{tabela}```')

        except Exception as e:
            await ctx.send(f"Erro: {e}")

    @commands.command(name="link", aliases=["retornar_link"])
    async def retornar_link(self, ctx):
        try:
            link = self.bot.planilha.retornar_link()
            await ctx.send(link)

        except Exception as e:
            await ctx.send(f"Erro: {e}")

    @commands.command(name="linha", aliases=["ler_linha"])
    async def ler_linha(self, ctx, nome):
        try:
            linha = self.bot.verificador.converter_nome_em_linha(nome)
            header, linha = self.bot.planilha.ler_linha(linha)
            tabela = self.bot.tabulacao.tabular(header, linha)
            await ctx.send(f'```{tabela}```')

        except (NomeInvalidoErro) as e:
            await ctx.send(e)

        except Exception as e:
            await ctx.send(f"Erro: {e}")

    
async def setup(bot):
    await bot.add_cog(ComandosPlanilha(bot))