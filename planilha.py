import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
SHEET_ID = os.getenv('SHEET_ID')
SHEET_URL = os.getenv('SHEET_URL')

class Planilha():
    def __init__(self):
        google_credenciais = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes = ["https://www.googleapis.com/auth/spreadsheets"])
        google_cliente = gspread.authorize(google_credenciais)
        p = google_cliente.open_by_key(SHEET_ID)
        self.planilha = p.get_worksheet(0)
        
    def escrever_valor(self, linha, coluna, valor):
        self.planilha.update_cell(linha, coluna, valor)
        return self.ler_linha(linha) # ineficiente
            
    def ler_tabela(self):
        tabela = self.planilha.get_all_values()
        header = tabela[0]
        return header, tabela[1:]
    
    def zerar_tabela(self):
        num_linhas = len(self.planilha.col_values(1))
        intervalo = f'B2:H{num_linhas}'
        valores = self.planilha.get_all_values()[1:] # Ignora a linha com os dias da semana
        novos_valores = [[int(0) for v in linha[1:8]] for linha in valores] # preenche com 0 tudo entre as colunas B e H 
        self.planilha.update(intervalo, novos_valores)
    
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
    
    def ler_linha(self, linha):
        tabela = self.planilha.get_all_values()
        header = tabela[0]
        linha_buscada = tabela[linha - 1]
       
        return header, [linha_buscada]
        
    def somar_valor(self, linha, coluna, valor):
        novo_valor = int(self.planilha.cell(linha, coluna).value) + int(valor)
        self.planilha.update_cell(linha, coluna, novo_valor)
        return self.ler_linha(linha) 