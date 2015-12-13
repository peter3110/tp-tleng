# Lista de tokens
tokens = [
    'ID',          # es hoja
    'DIVIDE',      # es nodo: /
    'LPAREN',      # es nodo: (
    'RPAREN',      # es nodo: )
    'LBRACKET',    # para separar expresiones sin agregar ningun simbolo
    'RBRACKET',    # para separar expresiones sin agregar ningun simbolo
    'SUPERINDEX',  # es nodo: ^
    'SUBINDEX'    # es nodo: _
]

# Expresiones regulares para cada token
t_ignore  = ' \t' # ignoramos los espacios
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_SUPERINDEX = r'\^'
t_SUBINDEX = r'\_'

def t_ID(t):
    r'[a-zA-Z0-9+-]'
    t.value = t.value
    return t


def t_error(t):
    message = "Token desconocido:"
    message += "\ntype:" + t.type
    message += "\nvalue:" + str(t.value)
    message += "\nline:" + str(t.lineno)
    message += "\nposition:" + str(t.lexpos)
    raise Exception(message)
