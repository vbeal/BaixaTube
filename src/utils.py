import re

def strip_ansi_codes(string):
    """
    Remove os códigos ANSI de escape de uma string.

    Parâmetros:
        string (str): A string contendo códigos ANSI de escape.

    Retorna:
        str: A string sem os códigos ANSI de escape.
    """
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', string)
