import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
from utils import converter_dia_em_numero

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
    

    def ler_valor(self, nome, dia):
        nome = nome.lower()
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos dias a seguir: {", ".join(dias)}"

        celula = self.planilha.find(nome)

        if celula:
            coluna = converter_dia_em_numero(dia)
            linha = celula.row
            valor = self.planilha.cell(linha, coluna).value
            return valor if valor else '0'

        else:
            return f"Nome {nome} não encontrado!"
        
    # TODO: retorno ineficiente (refaz a busca da linha) melhorar
    # TODO: tratar valor (pode ser caractere, pode ser número negativo, pode ser não inteiro)
    def escrever_valor(self, nome, dia, valor):
        nome = nome.lower()
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos nomes a seguir: {", ".join(dias)}"

        celula = self.planilha.find(nome)

        if celula:
            coluna = converter_dia_em_numero(dia)
            linha = celula.row
            self.planilha.update_cell(linha, coluna, valor)
            return self.ler_linha(nome) # ineficiente

        else:
            return f"Nome {nome} não encontrado!"


    def ler_tabela(self):
        tabela = self.planilha.get_all_values()
        header = tabela[0]
        return header, tabela[1:]
    
    def completar_zeros(self, valor_default = 0):
        num_linhas = len(self.planilha.col_values(1))
        intervalo = f'B2:H{num_linhas}'
        valores = self.planilha.get_all_values()[1:] # Ignora a linha com os dias da semana
        novos_valores = [[int(v) if v != '' else valor_default for v in linha[1:8]] for linha in valores] # preenche com <valor_default> onde não tiver nada entre as colunas B e H 
        self.planilha.update(intervalo, novos_valores)
        
        return True
    
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
        nome = nome.lower()

        tabela = self.planilha.get_all_values()
        header = tabela[0]

        for i in range(1, len(tabela) + 1):
            if i == 1: continue
            if tabela[i - 1][0] == nome:
                break

        if i <= len(tabela):
            return header, [tabela[i - 1]]

        else:
            return f"Nome {nome} não encontrado na planilha"
        
    # TODO: refatorar
    def escrever_linha(self, nome, valores = []):
        if valores or len(valores) > 7:
            for valor in valores:
                if type(valor) is not int or valor < 0:
                    return f"O valor {valor} é inválido."
                
            conversor_quantidade_coluna = {
                        1 : "B",
                        2 : "C",
                        3 : "D",
                        4 : "E",
                        5 : "F",
                        6 : "G",
                        7 : "H"
            }

            num_coluna = conversor_quantidade_coluna[len(valores)]

            celula = self.planilha.find(nome)
            intervalo = f'B{celula.row}:H{num_coluna}'
            celula = self.planilha.update(valores, intervalo)
            return self.ler_linha(nome)
            
        else:
            return f"Passe uma lista válida"
        
    def somar_valor(self, nome, dia, valor):
        nome = nome.lower()
        dia = dia.lower()

        if dia not in dias:
            return f"O dia {dia} é inválido. Tente um dos nomes a seguir: {", ".join(dias)}"

        celula = self.planilha.find(nome)

        if celula:
            coluna = converter_dia_em_numero(dia)
            linha = celula.row
            novo_valor = int(self.planilha.cell(linha, coluna).value) + int(valor)
            self.planilha.update_cell(linha, coluna, novo_valor)
            return self.ler_linha(nome) # ineficiente

        else:
            return f"Nome {nome} não encontrado!"