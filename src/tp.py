# -----------------------------------------------------------------------------
# tp.py
#
# -----------------------------------------------------------------------------
import lexer_rules
import parser_rules
import pdb

from sys import argv, exit

import ply.lex as lex
import ply.yacc as yacc

if __name__ == "__main__":
  # Build the lexer
  lexer = lex.lex(module=lexer_rules)
  # Build the parser
  parser = yacc.yacc(module=parser_rules)

  s = "init"
  while s != "exit()": # finalizo si en la entrada escriben exit() - asumimos que es una cadena no valida (?)
    try:
      s = raw_input('cadena > ')
    except EOFError:
      break
    if not s: continue
    ast = parser.parse(s, lexer)
    # TODO: implementar los recorrer y el dump, q van a hacer los distintos recorridos para implementar
    # el comportamiento de la TDS, la implementacion de los recorrer deberia vivir en la definicion de las clases
    ast.recorrer()
    ast.recorrer2()
    out = []
    out.append ( '''<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> <svg xmlns="http://www.w3.org/2000/svg" version="1.1"> <g transform="translate(0, 50) scale(50)" font-family= "Courier">''' )

    ast.dump_ast(out)

    out.append ( '''</g>
                    </svg> ''' )
    open('fig.svg','w').write(''.join(out))

    print out

# # ejemplo del tp: (A^BC^D/E^F_G+H)-I
# '''
#         <text x="0" y="0" font-size="1" transform=
#               "translate(0, 1.36875) scale(1,2.475)">(</text>
#         <text x=".69" y=".53" font-size="1">A</text>
#         <text x="1.29" y=".08" font-size=".7">B</text>
#         <text x="1.71" y=".53" font-size="1">C</text>
#         <text x="2.31" y=".08" font-size=".7">D</text>
#         <line x1="0.6" y1="0.72" x2="2.82" y2=".72"
#               stroke-width="0.03" stroke="black"/>
#         <text x="0.6" y="1.68" font-size="1">E</text>
#         <text x="1.2" y="1.93" font-size=".7">G</text>
#         <text x="1.2" y="1.23" font-size=".7">F</text>
#         <text x="1.62" y="1.68" font-size="1">+</text>
#         <text x="2.22" y="1.68" font-size="1">H</text>
#         <text x="0" y="0" font-size="1" transform =
#               "translate(2.82, 1.36875) scale(1,2.475)">)</text>
#         <text x="3.42" y="1" font-size="1">-</text>
#         <text x="4.02" y="1" font-size="1">I</text>
#     '''
