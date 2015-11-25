from lexer_rules import tokens

import pprint

# Mientras voy parseando, creo el arbol sintactico de la expresion.
nodos = { 'DIVIDE', 'CONCAT', 'SUPERINDEX', 'SUBINDEX',
  'SUBSUPERINDEX', 'SUPERSUBINDEX', 'ID', '()' }

# Los atributos con los que voy a ir decorando el arbol sintactico
atributosNil = { 'tam': None, 'x': None, 'y': None,
  'a': None, 'h1': None, 'h2': None}

def p_expression_init(p):
    'S : E'
    res1 = recorrer(p[1],1)     # agrego todos los atributos menos x e y
    res2 = recorrer2(res1,0.5,-0.7)  # agrego x e y
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

# Cada key del diccionario tiene como valor una tupla < hijos, atributos >

def recorrer(t,tactual):    # primer recorrido top-down (rellenar tam) +++ recorrido bottom-up (rellenar a, h1 y h2)

  t['attr']['h1'] = 0
  t['attr']['h2'] = 0

  if ('ID' in t.keys() ):
    t['attr']['tam'] = tactual
    t['attr']['a'] = t['attr']['tam'] * 0.6    # porque el ancho es 0.6 * tam

  if ( 'DIVIDE' in t.keys() ):
    t['attr']['tam'] = tactual * 2        # esto no se si esta bien. no depende de nom y denom ?
    elems = t.get('DIVIDE')
    nominador = recorrer(elems[0], tactual).copy()
    denominador = recorrer(elems[1], tactual).copy()

    nominador['attr']['a'] = elems[0]['attr']['a']
    denominador['attr']['a'] = elems[1]['attr']['a']

    ancho_divide = max(nominador['attr']['a'], denominador['attr']['a']) * 1
    t['attr']['a'] = ancho_divide # aca podria tener que agregar una *CTE. = 0.6 para emparejar con denominador / nominador-
                                  # Ahora, esto lo estoy haciendo cuando paso a escribir en el output el ancho de la linea de div.
    t['attr']['h1'] = tactual * 0.1
    t['attr']['h2'] = - tactual * 0.1 - denominador['attr']['tam']

  if ('()' in t.keys() ):
    t['attr']['tam'] = tactual    # este valor se lo pongo en la primera recorrida. en la 2da, lo modifico ( ? )
    elems = t.get('()')
    recorrer(elems[0],tactual)
    t['attr']['a'] = elems[0]['attr']['a'] * 1.05  # doy un margen a izq y derecha
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0

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
    t['attr']['h2'] = 0.2 * t['attr']['tam']

  if ('SUPERSUBINDEX' in t.keys() ):
    t['attr']['tam'] = 1.7 * tactual
    elems = t.get('SUPERSUBINDEX')
    h1 = recorrer(elems[0], tactual).copy()
    h2 = recorrer(elems[1], tactual * 0.7).copy()
    h3 = recorrer(elems[2], tactual * 0.7).copy()
    t['attr']['a'] = h1['attr']['a'] + max(h2['attr']['a'], h3['attr']['a'])
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0.2 * t['attr']['tam']

  if ('SUBSUPERINDEX' in t.keys() ):
    t['attr']['tam'] = 1.7 * tactual
    elems = t.get('SUBSUPERINDEX')
    h1 = recorrer(elems[0], tactual).copy()
    h2 = recorrer(elems[1], tactual * 0.7).copy()
    h3 = recorrer(elems[2], tactual * 0.7).copy()
    t['attr']['a'] = h1['attr']['a'] + max(h2['attr']['a'], h3['attr']['a'])
    t['attr']['h1'] = 0
    t['attr']['h2'] = 0.2 * t['attr']['tam']

  return t


def recorrer2(t, x, y): # segundo recorrido top-down, ahora para definir valores de x e y
                        # tambien modifico el tamanno de '()' para escalar lo que hay entre '()'

    t['attr']['x'] = x
    t['attr']['y'] = y

    #if ( 'ID' in t.keys() ):

    if ( 'DIVIDE' in t.keys() ):
        elems = t.get('DIVIDE')

        if (elems[0]['attr']['a'] < elems[1]['attr']['a']):
          h1 = recorrer2(elems[0], x + elems[1]['attr']['a'] * (0.3), t['attr']['y'] + t['attr']['h1'] + elems[0]['attr']['h2']).copy()   # desplazo segun h1, h2
        else:
          h1 = recorrer2(elems[0], x, t['attr']['y'] + t['attr']['h1'] + elems[0]['attr']['h2']).copy()

        if (elems[0]['attr']['a'] > elems[1]['attr']['a']):
          h2 = recorrer2(elems[1], x + elems[0]['attr']['a'] * (0.3), t['attr']['y'] - t['attr']['tam'] * 0.4).copy()  # tengo en cuenta el escalamiento para el denom
        else:
          h2 = recorrer2(elems[1], x, t['attr']['y'] - t['attr']['tam'] * 0.4).copy()


    if ( '()' in t.keys() ):

        elems = t.get('()')
        t['attr']['tam'] = elems[0]['attr']['tam']    # a '()' le pongo = tamanno que lo que hay adentro

        recorrer2(elems[0], x, y)   # faltaria desplazarse un poco por el '(' ?


    if ( 'CONCAT' in t.keys() ):
        elems = t.get('CONCAT')
        recorrer2(elems[0], x, y)
        recorrer2(elems[1], x + elems[0]['attr']['a'] , y)      # AGREGO CTE = 0.6 PARA DESPLAZAR A DERECHA  - OK

    if ( 'SUPERINDEX' in t.keys() ):
        elems = t.get('SUPERINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'], y + 0.3 * h1['attr']['tam'])


    if ( 'SUBINDEX' in t.keys() ):
        elems = t.get('SUBINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'], y - 0.3 * h1['attr']['tam'])   # ESTE 0.3 ES SUPER ARBITRARIO


    if ( 'SUPERSUBINDEX' in t.keys() ):
        elems = t.get('SUPERSUBINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'], y + 0.3 * h1['attr']['tam'])
        recorrer2(elems[2], x + elems[0]['attr']['a'], y - 0.3 * h1['attr']['tam'])

    if ( 'SUBSUPERINDEX' in t.keys() ):
        elems = t.get('SUBSUPERINDEX')
        h1 = recorrer2(elems[0], x, y).copy()
        recorrer2(elems[1], x + elems[0]['attr']['a'], y - 0.3 * h1['attr']['tam'])
        recorrer2(elems[2], x + elems[0]['attr']['a'], y + 0.3 * h1['attr']['tam'])


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


###
def recorrer3(t, out):

  if ( '()' in t.keys() ):
    elems = t.get('()')
    out.append ( make_open_paren(str(elems[0]['attr']['x']), str(-elems[0]['attr']['y']), # ejes x, y
                                 str(elems[0]['attr']['tam']),                            # font - size
                                 str(-elems[0]['attr']['tam'] * 0.3 ),str(0),   # retocar para que quede "lindo", translate x, translate y
                                 str(1),str(1)) )     # scale x    , scale y
    recorrer3(elems[0], out)
    out.append ( make_close_paren(str(elems[0]['attr']['x']), str(-elems[0]['attr']['y']),
                                  str(elems[0]['attr']['tam']),
                                  str(elems[0]['attr']['a'] ),str(0),       # retocar para que quede "lindo"
                                  str(1),str(1)) )

  if ( 'DIVIDE' in t.keys() ):
    elems = t.get('DIVIDE')
    recorrer3(elems[0], out)

    out.append( make_line(str(t['attr']['x']), str(-t['attr']['y']),
                          str(t['attr']['x'] + t['attr']['a']), # recien aca balanceo el largo de la linea de div.
                          str(-t['attr']['y']), str(0.03 * t['attr']['tam'])) )  # harcodeo el ancho de la linea de division

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


