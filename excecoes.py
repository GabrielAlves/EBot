class NomeInvalidoErro(Exception):
    def __init__(self, nome, nomes_validos = None):
        msg = f"Nome '{nome}' não encontrado na planilha!"
        
        if nomes_validos: 
            nomes_validos_str = ", ".join(nomes_validos)
            msg += f"\nNomes válidos: {nomes_validos_str}."
        
        super().__init__(msg)

class DiaInvalidoErro(Exception):
    def __init__(self, dia, dias_validos = None):
        msg = f"Dia '{dia}' não encontrado na planilha!"
        
        if dias_validos: 
            dias_validos_str = ", ".join(dias_validos)
            msg += f"\nDias válidos: {dias_validos_str}."
        
        super().__init__(msg)

class AbreviacaoInvalidaErro(Exception):
    def __init__(self, abrev, abrev_validas = None):
        msg = f"Abreviação '{abrev}' não encontrada!"

        if abrev_validas:
            abrev_validas_str = ", ".join(abrev_validas)
            msg += f"\nAbreviações válidas: {abrev_validas_str}."

        super().__init__(msg)        

class ValorInvalidoErro(Exception):
    def __init__(self, valor, pos = ""):
        if pos:
            msg = f"O valor na posição {pos} deve ser um inteiro positivo! Foi fornecido '{valor}'"
        else:
            msg = f"O valor deve ser um inteiro positivo! Foi fornecido '{valor}'"
        super().__init__(msg)

class QuantidadeInvalidaErro(Exception):
    def __init__(self, valor):
            msg = f"Podem ser fornecidos no máximo 7 valores! Foram fornecidos '{valor}' valores"
            super().__init__(msg)