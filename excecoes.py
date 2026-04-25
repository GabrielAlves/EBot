class NomeInvalidoErro(Exception):
    def __init__(self, nome):
        super().__init__(f"Nome '{nome}' não encontrado na planilha!")

class DiaInvalidoErro(Exception):
    def __init__(self, dia):
        super().__init__(f"Dia '{dia}' não encontrado na planilha!")

class ValorInvalidoErro(Exception):
    def __init__(self, valor):
        super().__init__(f"Valor '{valor}' deve ser um inteiro positivo!")