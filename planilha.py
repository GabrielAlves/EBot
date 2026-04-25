import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
from dias import converter_dia_em_numero
from excecoes import NomeInvalidoErro, DiaInvalidoErro

load_dotenv()

GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
SHEET_ID = os.getenv('SHEET_ID')
SHEET_URL = os.getenv('SHEET_URL')

escopos = [
    "https://www.googleapis.com/auth/spreadsheets"
]

dias = ['domingo', 
        'segunda',
        'terca',
        'quarta',
        'quinta',
        'sexta',
        'sabado']

# TODO: tratar o erro de quando sheet_commands espera dois valores (header e tabela), mas recebe um (string de erro)
class Planilha():
    def __init__(self):
        google_credenciais = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes = escopos)
        google_cliente = gspread.authorize(google_credenciais)
        p = google_cliente.open_by_key(SHEET_ID)
        self.planilha = p.get_worksheet(0)
        
    # TODO: retorno ineficiente (refaz a busca da linha) melhorar
    # TODO: tratar valor (pode ser caractere, pode ser número negativo, pode ser não inteiro)
    def escrever_valor(self, nome, dia, valor):
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos nomes a seguir: {", ".join(dias)}"

        linha = self.buscar_nome_planilha(nome)
        coluna = converter_dia_em_numero(dia)
        self.planilha.update_cell(linha, coluna, valor)
        return self.ler_linha(nome) # ineficiente
            
    def ler_tabela(self):
        tabela = self.planilha.get_all_values()
        header = tabela[0]
        return header, tabela[1:]
    
    def zerar_tabela(self, valor_default = 0):
        num_linhas = len(self.planilha.col_values(1))
        intervalo = f'B2:H{num_linhas}'
        valores = self.planilha.get_all_values()[1:] # Ignora a linha com os dias da semana
        novos_valores = [[int(valor_default) for v in linha[1:8]] for linha in valores] # preenche com <valor_default> onde não tiver nada entre as colunas B e H 
        self.planilha.update(intervalo, novos_valores)
        
        return True
    
    def gerar_placar(self):
        tabela = self.planilha.get_all_values()

        header = tabela[0][0], tabela[0][8]
        nomes_e_total = [[linha[0], linha[8]] for linha in tabela[1:]] # Pega as colunas dos nomes e tempo total
        placar = sorted(nomes_e_total, key = lambda x : int(x[1]), reverse = True)
        return header, placar
    
    def farmar_aura(self):
        header, placar = self.gerar_placar()
        return header, [placar[0]]
    
    def retornar_link(self):
        return SHEET_URL
    
    def ler_linha(self, nome):
        tabela = self.planilha.get_all_values()
        header = tabela[0]

        linha = self.buscar_nome_planilha(nome)
        linha_buscada = tabela[linha - 1]
       
        return header, [linha_buscada]
        
    def somar_valor(self, nome, dia, valor):
        #nome = nome.lower()
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos nomes a seguir: {", ".join(dias)}"

        celula = self.planilha.find(nome, case_sensitive = False)

        if celula:
            coluna = converter_dia_em_numero(dia)
            linha = celula.row
            novo_valor = int(self.planilha.cell(linha, coluna).value) + int(valor)
            self.planilha.update_cell(linha, coluna, novo_valor)
            return self.ler_linha(nome) # ineficiente

        else:
            return f"Nome {nome} não encontrado!"
        
    def buscar_nome_planilha(self, nome_buscado):
        nome_buscado = nome_buscado.lower()
        nomes = self.planilha.col_values(1)

        # linha representa a linha dentro da planilha do google sheets
        for linha in range(2, len(nomes) + 1):
            nome = nomes[linha - 1].lower()

            if nome == nome_buscado:
                return linha

        raise NomeInvalidoErro(nome_buscado)