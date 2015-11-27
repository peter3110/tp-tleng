# List of token names.   This is always required
tokens = (
   'ID',          # es hoja
   'DIVIDE',      # es nodo: /
   'LPAREN',
   'RPAREN',
   'LBRACKET',    # es nodo: ()
   'RBRACKET',
   'SUPERINDEX',  # es nodo: ^
   'SUBINDEX',     # es nodo: _
)

# Regular expression rules for simple tokens
t_ignore  = ' \t'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_SUPERINDEX = r'\^'
t_SUBINDEX = r'_'
def t_ID(t):
    r'[a-zA-Z+-]'
    t.value = t.value
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
