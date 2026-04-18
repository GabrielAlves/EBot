import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
from utils import converter_dia_em_numero

load_dotenv()

GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
SHEET_ID = os.getenv('SHEET_ID')
SHEET_URL = os.getenv('SHEET_URL')

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

dias = ['domingo', 
        'segunda',
        'terca',
        'quarta',
        'quinta',
        'sexta',
        'sabado']

class Sheet():
    def __init__(self):
        google_creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes = scopes)
        google_client = gspread.authorize(google_creds)
        sh = google_client.open_by_key(SHEET_ID)
        self.sheet = sh.get_worksheet(0)
    

    def ler_valor(self, nome, dia):
        nome = nome.lower()
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos dias a seguir: {", ".join(dias)}"

        celula = self.sheet.find(nome)

        if celula:
            coluna = converter_dia_em_numero(dia)
            linha = celula.row
            valor = self.sheet.cell(linha, coluna).value
            return valor if valor else '0'

        else:
            return f"Nome {nome} não encontrado!"
        
    # TODO: retornar a linha atualizada em vez do valor
    def escrever_valor(self, nome, dia, valor):
        nome = nome.lower()
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos nomes a seguir: {", ".join(dias)}"

        celula = self.sheet.find(nome)

        if celula:
            coluna = converter_dia_em_numero(dia)
            linha = celula.row
            self.sheet.update_cell(linha, coluna, valor)
            return valor if valor else '0'

        else:
            return f"Nome {nome} não encontrado!"


    def ler_tabela(self):
        tabela = self.sheet.get_all_values()
        header = tabela[0]
        return header, tabela[1:]
    
    def preencher_vazios(self, valor_default = 0):
        num_linhas = len(self.sheet.col_values(1))
        intervalo = f'B2:H{num_linhas}'
        valores = self.sheet.get_all_values()[1:] # Ignora a linha com os dias da semana
        novos_valores = [[int(v) if v != '' else valor_default for v in linha[1:8]] for linha in valores] # preenche com <valor_default> onde não tiver nada entre as colunas B e H 
        self.sheet.update(intervalo, novos_valores)
        
        return True
    
    def limpar_tabela(self, valor_default = 0):
        num_linhas = len(self.sheet.col_values(1))
        intervalo = f'B2:H{num_linhas}'
        valores = self.sheet.get_all_values()[1:] # Ignora a linha com os dias da semana
        novos_valores = [[int(valor_default) for v in linha[1:8]] for linha in valores] # preenche com <valor_default> onde não tiver nada entre as colunas B e H 
        self.sheet.update(intervalo, novos_valores)
        
        return True
    
    def gerar_placar(self):
        tabela = self.sheet.get_all_values()

        header = tabela[0][0], tabela[0][8]
        nomes_e_total = [[linha[0], linha[8]] for linha in tabela[1:]] # Pega as colunas dos nomes e tempo total
        placar = sorted(nomes_e_total, key = lambda x : int(x[1]), reverse = True)
        return header, placar
    
    def farmar_aura(self):
        header, placar = self.gerar_placar()
        return header, [placar[0]]
    
    def retornar_link(self):
        return SHEET_URL