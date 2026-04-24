from tabulate import tabulate

class Tabulacao:
    def __init__(self):
        self.alinhamentos = ("left", "right", "right", "right", "right", "right", "right", "right", "right")
        self.formato = 'pretty'
    
    def tabular(self, tabela, header, num_colunas = 9):
        return tabulate(tabela, header, colalign= self.alinhamentos[:num_colunas], tablefmt=self.formato)