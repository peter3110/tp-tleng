from lexer_rules import tokens

from expressions import *

import pprint

def p_expression_init(subexpressions):
  'S : E'
  subexpressions[0] = Start(subexpressions[1])

# E -> E / A | A
def p_expression_E1(subexpressions):
  'E : E DIVIDE A'
  subexpressions[0] = Divide(subexpressions[1], subexpressions[3])

def p_expression_E2(subexpressions):
  'E : A'
  subexpressions[0] = subexpressions[1]

# A -> A B | B
def p_expression_A1(subexpressions):
  'A : A B'
  subexpressions[0] = Concat(subexpressions[1], subexpressions[2])

def p_expression_A2(subexpressions):
  'A : B'
  subexpressions[0] = subexpressions[1]

# B -> C | C SUPERINDEX C | C SUBINDEX C | C SUPERINDEX C SUBINDEX C | C SUBINDEX C SUPERINDEX C
def p_expression_B1(subexpressions):
  'B : C'
  subexpressions[0] = subexpressions[1]

def p_expressionB2(subexpressions):
  'B : C SUPERINDEX C'
  subexpressions[0] = SuperIndex(subexpressions[1], subexpressions[3])

def p_expressionB3(subexpressions):
  'B : C SUBINDEX C'
  subexpressions[0] = SubIndex(subexpressions[1], subexpressions[3])

def p_expressionB4(subexpressions):
  'B : C SUPERINDEX C SUBINDEX C'
  subexpressions[0] = SuperSubIndex(subexpressions[1], subexpressions[3], subexpressions[5])

def p_expressionB5(subexpressions):
  'B : C SUBINDEX C SUPERINDEX C'
  subexpressions[0] = SubSuperIndex(subexpressions[1], subexpressions[3], subexpressions[5])

# C -> { E }
def p_expression_C1(subexpressions):
  'C : LBRACKET E RBRACKET'
  subexpressions[0] = subexpressions[2]

# C -> ( E )
def p_expression_C2(subexpressions):
  'C : LPAREN E RPAREN'
  subexpressions[0] = Parenthesis(subexpressions[2])

# C -> ID
# tengo que escribir el valor del token ID
def p_expression_C3(subexpressions):
  'C : ID'
  subexpressions[0] = Id(subexpressions[1])

# Error rule for syntax errors
def p_error(p):
  raise Exception("Syntax error.")
