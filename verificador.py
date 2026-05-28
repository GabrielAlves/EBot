from excecoes import *

class Verificador:
    def __init__(self, planilha):
        self.p = planilha

        self.dias = [
                    'domingo', 
                    'segunda',
                    'terca',
                    'quarta',
                    'quinta',
                    'sexta',
                    'sabado'
                    ]
        
        self.abreviacoes = {
                            "dom" : "domingo",
                            "seg" : "segunda",
                            "ter" : "terca",
                            "qua" : "quarta",
                            "qui" : "quinta",
                            "sex" : "sexta",
                            "sab" : "sabado"
                            }
                            
    
    def converter_dia_em_coluna(self, dia):
        dia = dia.lower()

        for coluna, nome in enumerate(self.dias, start = 2):
            if nome == dia:
                return coluna
            
        raise DiaInvalidoErro(dia, self.dias)
    
    def verificar_dia(self, dia):
        dia = dia.lower()

        for d in self.dias:
            if d == dia:
                return True
            
        raise DiaInvalidoErro(dia, self.dias)
    
    def verificar_abreviacao(self, abrev):
        abrev = abrev.lower()

        for a in self.abreviacoes:
            if abrev == a:
                return self.abreviacoes[abrev]
            
        raise AbreviacaoInvalidaErro(abrev, list(self.abreviacoes))
    
    def converter_nome_em_linha(self, nome):
        nome = nome.lower()
        nomes = self.p.planilha.col_values(1)

        for linha in range(2, len(nomes) + 1):
            n = nomes[linha - 1].lower()
            n = n[:len(nome)]

            if nome == n:
                return linha

        raise NomeInvalidoErro(nome, nomes[1:])
    
    def verificar_valor(self, valor):
        try:
            valor = int(valor)
            if valor < 0:
                raise ValorInvalidoErro(valor)
            
            return True
        except (TypeError, ValueError):
            raise ValorInvalidoErro(valor)