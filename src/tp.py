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

    ast.recorrer()
    ast.recorrer2()

    out = []
    ast.dump_ast(out)

    open('fig.svg','w').write(''.join(out))

    print out
