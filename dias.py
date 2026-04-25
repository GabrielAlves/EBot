from excecoes import DiaInvalidoErro

class Dias:
    def __init__(self):
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
                            
    
    def converter_dia_em_numero(self, dia):
        dia = dia.lower()

        for num, nome in enumerate(self.dias, start = 2):
            if nome == dia:
                return num
            
        raise DiaInvalidoErro(dia)

# Os dias da semana começama a partir da coluna 2 na planilha
def converter_dia_em_numero(dia):
    dia = dia.lower()
    dias = ['domingo', 
                'segunda',
                'terca',
                'quarta',
                'quinta',
                'sexta',
                'sabado']

    for num, nome in enumerate(dias, start = 2):
        if nome == dia:
            return num
        
    return None