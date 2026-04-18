from tabulate import tabulate

class Tabulacao:
    def __init__(self):
        self.colalign = ("left", "right", "right", "right", "right", "right", "right", "right", "right")
        self.tablefmt = 'pretty'
    
    def tabular(self, tabela, header, num_colunas = 9):
        colalign_aux = self.colalign[:num_colunas]
        return tabulate(tabela, header, colalign= colalign_aux, tablefmt=self.tablefmt)