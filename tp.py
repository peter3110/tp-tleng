# -----------------------------------------------------------------------------
# tp.py
#
# -----------------------------------------------------------------------------

# ------------------------- LEXER -------------------------
import ply.lex as lex

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
t_SUBINDEX = r'_'  # TODO: no entiendo por que, NO ANDA con el guion bajo: _ 
def t_ID(t):
    r'[a-zA-Z+]'    # TODO: esto podria ser cualquier simbolo en realidad Faltan agregar muchos simbolos
    t.value = t.value  
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
#data = '''(A_B^C{IID})'''
#lexer.input(data)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: 
#        break      # No more input
#    print(tok)

# ------------------------- PARSER -------------------------

import ply.yacc as yacc
import pprint

# Mientras voy parseando, creo el arbol sintactico de la expresion.
nodos = { 'DIVIDE', 'CONCAT', 'SUPERINDEX', 'SUBINDEX',
    'SUBSUPERINDEX', 'SUPERSUBINDEX', 'ID', '()' }

atributosNil = { 'tam': None, 'x': None, 'y': None, 
  'a': None, 'h1': None, 'h2': None}

# Cada key del diccionario tiene como valor una tupla < hijos, atributos >

def recorrer(t,tactual):    # primer recorrido top-down (rellenar tam) + recorrido bottom-up (rellenar a, h1 y h2)

  t['attr']['h1'] = 0
  t['attr']['h2'] = 0    

  if ( 'DIVIDE' in t.keys() ):
    t['attr']['tam'] = tactual * 2        # esto no se si esta bien. no depende de nom y denom ?
    elems = t.get('DIVIDE')
    nominador = recorrer(elems[0], tactual).copy()
    denominador = recorrer(elems[1], tactual).copy()
    ancho_divide = max(nominador['attr']['a'], denominador['attr']['a']) * 1
    nominador['attr']['a'] = ancho_divide
    denominador['attr']['a'] = ancho_divide
    t['attr']['a'] = ancho_divide * 0.6    # AGREGO CTE. = 0.6 para emparejar con denominador / nominador- OK
    t['attr']['h1'] = tactual * 0.1
    t['attr']['h2'] = - tactual * 0.1 - denominador['attr']['tam']

  if ('CONCAT' in t.keys() ):
    t['attr']['tam'] = tactual
    ancho_concat = 0
    for elem in t.get('CONCAT'): 
        h = recorrer(elem, tactual).copy()
        ancho_concat += h['attr']['a']
        t['attr']['tam'] = max(t['attr']['tam'], h['attr']['tam'])  # ACTUALIZO EL TAMANNO DE LA CONCATENACION
    t['attr']['a'] = ancho_concat
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0
  
  if ('SUPERINDEX' in t.keys() ):
    t['attr']['tam'] = 1.7 * tactual
    elems = t.get('SUPERINDEX')
    h1 = recorrer(elems[0], tactual).copy()
    h2 = recorrer(elems[1], tactual * 0.7).copy()
    t['attr']['a'] = h1['attr']['a'] + h2['attr']['a']
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0

  if ('SUBINDEX' in t.keys() ):
    t['attr']['tam'] = 1.7 * tactual
    elems = t.get('SUBINDEX')
    h1 = recorrer(elems[0], tactual).copy()
    h2 = recorrer(elems[1], tactual * 0.7).copy()
    t['attr']['a'] = h1['attr']['a'] + h2['attr']['a']
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0

  if ('SUPERSUBINDEX' in t.keys() ):
    t['attr']['tam'] = 1.7 * tactual
    elems = t.get('SUPERSUBINDEX')
    h1 = recorrer(elems[0], tactual).copy()
    h2 = recorrer(elems[1], tactual * 0.7).copy()
    h3 = recorrer(elems[2], tactual * 0.7).copy()
    t['attr']['a'] = h1['attr']['a'] + h2['attr']['a'] + h3['attr']['a']
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0

  if ('SUBSUPERINDEX' in t.keys() ):
    t['attr']['tam'] = 1.7 * tactual
    elems = t.get('SUBSUPERINDEX')
    h1 = recorrer(elems[0], tactual).copy()
    h2 = recorrer(elems[1], tactual * 0.7).copy()
    h3 = recorrer(elems[2], tactual * 0.7).copy()
    t['attr']['a'] = h1['attr']['a'] + h2['attr']['a'] + h3['attr']['a']
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0
  
  if ('()' in t.keys() ):
    t['attr']['tam'] = tactual
    elems = t.get('()')
    recorrer(elems[0],tactual)
    t['attr']['a'] = t['attr']['tam']
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0

  if ('ID' in t.keys() ):
    t['attr']['tam'] = tactual
    t['attr']['a'] = t['attr']['tam']

  return t


def recorrer2(t, x, y): # segundo recorrido top-down, ahora para definir valores de x e y

    t['attr']['x'] = x
    t['attr']['y'] = y

    #if ( 'ID' in t.keys() ):

    if ( 'DIVIDE' in t.keys() ):
        elems = t.get('DIVIDE')
        h1 = recorrer2(elems[0], x, t['attr']['y'] + t['attr']['h1'] ).copy()   # aca entran h1 y h2 en juego

        recorrer2(elems[1], x, t['attr']['y'] - elems[1]['attr']['tam'] * 0.7)

    if ( '()' in t.keys() ):
        elems = t.get('()')
        recorrer2(elems[0], x, y)   # faltaria desplazarse un poco por el '(' ?

    if ( 'CONCAT' in t.keys() ):
        elems = t.get('CONCAT')
        recorrer2(elems[0], x, y)
        recorrer2(elems[1], x + elems[0]['attr']['a'] * 0.6 , y)      # AGREGO CTE = 0.6 PARA DESPLAZAR A DERECHA  - OK

    if ( 'SUPERINDEX' in t.keys() ):
        elems = t.get('SUPERINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'] * 0.6, y + 0.5 * h1['attr']['tam'])


    if ( 'SUBINDEX' in t.keys() ):
        elems = t.get('SUBINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'] * 0.6, y - 0.5 * h1['attr']['tam'])   # ESTE 0.3 ES SUPER ARBITRARIO

    if ( 'SUPERSUBINDEX' in t.keys() ):
        elems = t.get('SUPERSUBINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'] * 0.6, y + 0.5 * h1['attr']['tam'])
        recorrer2(elems[2], x + elems[0]['attr']['a'] * 0.6, y - 0.5 * h1['attr']['tam'])

    if ( 'SUBSUPERINDEX' in t.keys() ):
        elems = t.get('SUBSUPERINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'] * 0.6, y - 0.5 * h1['attr']['tam'])
        recorrer2(elems[2], x + elems[0]['attr']['a'] * 0.6, y + 0.5 * h1['attr']['tam'])


    return t



# === Parseo ====

def make_text(x,y,tam,char):
  return '''<text x="''' + x + '''" y="''' + y + '''" font-size="''' + tam + '''">''' + char + '''</text>'''

def make_line(x1,y1,x2,y2,ancho):
  return '''<line x1="''' + x1 + '''" y1="''' + y1 + '''" x2="''' + x2 + '''" y2="''' + y2 + '''" stroke-width="''' + ancho + '''" stroke="black"/>'''

def make_open_paren(x,y,tam,t1,t2,s1,s2):
  return '''<text x="''' + x + '''" y="''' + y + '''" font-size="''' + tam + '''" transform="translate(''' + t1 + ''',''' + t2 + ''') scale(''' + s1 + ''',''' + s2 + ''')">(</text>'''

def make_close_paren(x,y,tam,t1,t2,s1,s2):
  return '''<text x="''' + x + '''" y="''' + y + '''" font-size="''' + tam + '''" transform="translate(''' + t1 + ''',''' + t2 + ''') scale(''' + s1 + ''',''' + s2 + ''')">)</text>'''


def recorrer3(t, out):
  #out.append( make_text('0.69','0', '1', 'A') )
  #out.append( make_text('1.29','0', '1', 'B') )

  if ( 'DIVIDE' in t.keys() ):
    elems = t.get('DIVIDE')
    recorrer3(elems[0], out)

    out.append( make_line(str(t['attr']['x']), str(-t['attr']['y']), 
                          str(t['attr']['x'] + t['attr']['a']), str(-t['attr']['y']), '0.03') )  # harcodeo el ancho de la linea de division
    
    recorrer3(elems[1], out)

  if ( 'ID' in t.keys() ):
    out.append ( make_text(str(t['attr']['x']), str(-t['attr']['y']),   # me muevo al reves sobre el eje y
                           str(t['attr']['tam']), str(t['ID']) ) )

  if ( 'CONCAT' in t.keys() ):
    elems = t.get('CONCAT')
    recorrer3(elems[0], out)
    recorrer3(elems[1], out)

  if ( 'SUPERINDEX' in t.keys() ):
    elems = t.get('SUPERINDEX')
    recorrer3(elems[0], out)
    recorrer3(elems[1], out)

  if ( 'SUBINDEX' in t.keys() ):
    elems = t.get('SUBINDEX')
    recorrer3(elems[0], out)
    recorrer3(elems[1], out)

  if ( 'SUPERSUBINDEX' in t.keys() ):
    elems = t.get('SUPERSUBINDEX')
    recorrer3(elems[0], out)
    recorrer3(elems[1], out)
    recorrer3(elems[2], out)

  if ( 'SUBSUPERINDEX' in t.keys() ):
    elems = t.get('SUBSUPERINDEX')
    recorrer3(elems[0], out)
    recorrer3(elems[1], out)
    recorrer3(elems[2], out)


  # No esta andando por ahora
  if ( '()' in t.keys() ):
    elems = t.get('()')
    #out.append ( make_open_paren(str(elems[0]['attr']['x']), str(elems[0]['attr']['y']), str(elems[0]['attr']['tam']), 
    #                  str(0),str(1.3),str(1),str(2.4)) )
    recorrer3(elems[0], out)
    #out.append ( make_close_paren(str(elems[0]['attr']['x']), str(elems[0]['attr']['y']), str(elems[0]['attr']['tam']), 
    #                  str(0),str(1.3),str(1),str(2.4)) )



# ejemplo del tp: (A^BC^D/E^F_G+H)-I
''' 
        <text x="0" y="0" font-size="1" transform= 
              "translate(0, 1.36875) scale(1,2.475)">(</text>
        <text x=".69" y=".53" font-size="1">A</text>
        <text x="1.29" y=".08" font-size=".7">B</text>
        <text x="1.71" y=".53" font-size="1">C</text>
        <text x="2.31" y=".08" font-size=".7">D</text>
        <line x1="0.6" y1="0.72" x2="2.82" y2=".72" 
              stroke-width="0.03" stroke="black"/>
        <text x="0.6" y="1.68" font-size="1">E</text>
        <text x="1.2" y="1.93" font-size=".7">G</text> 
        <text x="1.2" y="1.23" font-size=".7">F</text>
        <text x="1.62" y="1.68" font-size="1">+</text>
        <text x="2.22" y="1.68" font-size="1">H</text>
        <text x="0" y="0" font-size="1" transform =
              "translate(2.82, 1.36875) scale(1,2.475)">)</text>
        <text x="3.42" y="1" font-size="1">-</text>
        <text x="4.02" y="1" font-size="1">I</text>
    '''

def p_expression_init(p):
    'S : E'
    res1 = recorrer(p[1],1)     # agrego todos los atributos menos x e y
    res2 = recorrer2(res1,0.5,0)  # agrego x e y
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(res2)

    out = []
    out.append ( '''<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> <svg xmlns="http://www.w3.org/2000/svg" version="1.1"> <g transform="translate(0, 200) scale(200)" font-family= "Courier">''' )

    # recorro el arbol y voy agregando lineas al output segun corresponda
    
    recorrer3(res2, out)

    # fin
    out.append ( '''</g>
                    </svg> ''' )
    open('test.svg','w').write(''.join(out))
    print out

# E -> E / A | A
def p_expression_E1(p):
    'E : E DIVIDE A'
    p[0] = { 'DIVIDE': [ p[1], p[3] ], 'attr': atributosNil.copy() }

def p_expression_E2(p):
    'E : A'
    p[0] = p[1]

# A -> A B | B
def p_expression_A1(p):
    'A : A B'
    p[0] = { 'CONCAT': [ p[1], p[2] ], 'attr': atributosNil.copy() }

def p_expression_A2(p):
    'A : B'
    p[0] = p[1]

# B -> C | C SUPERINDEX C | C SUBINDEX C | C SUPERINDEX C SUBINDEX C | C SUBINDEX C SUPERINDEX C
def p_expression_B1(p):
    'B : C'
    p[0] = p[1]

def p_expressionB2(p):
    'B : C SUPERINDEX C'
    p[0] = { 'SUPERINDEX': [ p[1], p[3] ], 'attr': atributosNil.copy() }

def p_expressionB3(p):
    'B : C SUBINDEX C'
    p[0] = { 'SUBINDEX': [ p[1], p[3] ], 'attr': atributosNil.copy() }

def p_expressionB4(p):
    'B : C SUPERINDEX C SUBINDEX C'
    p[0] = { 'SUPERSUBINDEX': [ p[1], p[3], p[5] ], 'attr': atributosNil.copy() }

def p_expressionB5(p):
    'B : C SUBINDEX C SUPERINDEX C'
    p[0] = { 'SUBSUPERINDEX': [ p[1], p[3], p[5] ], 'attr': atributosNil.copy() }

# C -> { E }
def p_expression_C1(p):
    'C : LBRACKET E RBRACKET'
    p[0] = p[2]

# C -> ( E )
def p_expression_C2(p):
    'C : LPAREN E RPAREN'
    p[0] = { '()': [ p[2] ], 'attr': atributosNil.copy() }

# C -> ID
# tengo que escribir el valor del token ID
def p_expression_C3(p):
    'C : ID'
    p[0] = { 'ID': p[1] , 'attr': atributosNil.copy() }



# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('cadena > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)



