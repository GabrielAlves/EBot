class Utils:
    def pegar_prefixo(bot, msg):
        nome_bot = bot.user.name if bot.user else "bot"
        return nome_bot + " "


def get_prefix(bot, msg):
    bot_name = bot.user.name if bot.user else "bot"
    return bot_name + " "

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