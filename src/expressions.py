k1 = 0.6
k2 = 0.6
c = 0.1

def initialize_atts(obj):
  obj.tam = 0
  obj.ancho = 0
  obj.altura = 0
  obj.x = 0
  obj.y = 0
  obj.h_up = 0
  obj.h_down = 0

def make_text(x,y,tam,char):
  return '''<text x="''' + x + '''" y="''' + y + '''" font-size="''' + tam + '''">''' + char + '''</text>'''

def make_line(x1,y1,x2,y2,ancho):
  return '''<line x1="''' + x1 + '''" y1="''' + y1 + '''" x2="''' + x2 + '''" y2="''' + y2 + '''" stroke-width="''' + ancho + '''" stroke="black"/>'''

def make_open_paren(x,y,tam,t1,t2,s1,s2):
  return '''<text x="''' + x + '''" y="''' + y + '''" font-size="''' + tam + '''" transform="translate(''' + t1 + ''',''' + t2 + ''') scale(''' + s1 + ''',''' + s2 + ''')">(</text>'''

def make_close_paren(x,y,tam,t1,t2,s1,s2):
  return '''<text x="''' + x + '''" y="''' + y + '''" font-size="''' + tam + '''" transform="translate(''' + t1 + ''',''' + t2 + ''') scale(''' + s1 + ''',''' + s2 + ''')">)</text>'''

class Start(object):
  def __init__(self, hijo):
    initialize_atts(self)
    self.hijo = hijo

  def name(self):
    return "Start"

  def children(self):
    return [self.hijo]

  def recorrer(self):
    self.hijo.tam = 1
    self.hijo.recorrer()

  def recorrer2(self):
    self.hijo.recorrer2()
    self.ancho = self.hijo.ancho
    self.h_up = self.hijo.h_up
    self.h_down = self.hijo.h_down
    self.altura = self.hijo.altura

  def dump_ast(self, out):
    self.hijo.x = 0
    self.hijo.y = self.h_up
    self.hijo.dump_ast(out)





class Divide(object):
  def __init__(self, numerador, denominador):
    initialize_atts(self)
    self.numerador = numerador
    self.denominador = denominador

  def name(self):
    return "Divide"

  def children(self):
    return [self.numerador, self.denominador]

  def recorrer(self):
    self.numerador.tam = self.tam
    self.numerador.recorrer()
    self.denominador.tam = self.tam
    self.denominador.recorrer()

  def recorrer2(self):
    self.numerador.recorrer2()
    self.denominador.recorrer2()
    self.ancho = max(self.denominador.ancho, self.numerador.ancho)
    self.h_up = self.numerador.altura + 0.40 * self.tam
    self.h_down = self.denominador.altura + 0.28 * self.tam
    self.altura = self.h_up + self.h_down

  def dump_ast(self, out):
    self.numerador.x = self.x + self.ancho/2 - self.numerador.ancho/2
    self.numerador.y = self.y - (self.numerador.h_down + 0.2 * self.tam)
    self.numerador.dump_ast(out)

    out.append( make_line(str(self.x), str(self.y), str(self.x + self.ancho), str(self.y), str(0.05) ) )

    self.denominador.x = self.x + self.ancho/2 - self.denominador.ancho/2
    self.denominador.y = self.y + (self.denominador.h_up + 0.1 * self.tam)
    self.denominador.dump_ast(out)





class Concat(object):
  def __init__(self, left, right):
    initialize_atts(self)
    self.left = left
    self.right = right

  def name(self):
    return "Concat"

  def children(self):
    return [self.left, self.right]

  def recorrer(self):
    self.left.tam = self.tam
    self.left.recorrer()
    self.right.tam = self.tam
    self.right.recorrer()

  def recorrer2(self):
    self.left.recorrer2()
    self.right.recorrer2()
    self.ancho = self.left.ancho + self.right.ancho
    # CHECK CHECK
    self.h_up = max(self.left.h_up, self.right.h_up)
    self.h_down = max(self.left.h_down, self.right.h_down)
    self.altura = self.h_down + self.h_up

  def dump_ast(self, out):
    self.left.x = self.x
    self.left.y = self.y
    self.left.dump_ast(out)

    self.right.x = self.x + self.left.ancho
    self.right.y = self.y
    self.right.dump_ast(out)




class SuperIndex(object):
  def __init__(self, base, index):
    initialize_atts(self)
    self.base = base
    self.index = index

  def name(self):
    return "SuperIndex"

  def children(self):
    return [self.base, self.index]

  def recorrer(self):
    self.base.tam = self.tam
    self.base.recorrer()
    self.index.tam = self.tam * 0.7
    self.index.recorrer()

  def recorrer2(self):
    self.base.recorrer2()
    self.index.recorrer2()
    self.ancho = self.base.ancho + self.index.ancho
    # CHECK CHECK
    self.h_up = self.base.h_up + self.index.altura * 0.7
    self.h_down = self.base.h_down
    self.altura = self.h_down + self.h_up

  def dump_ast(self, out):
    self.base.x = self.x
    self.base.y = self.y
    self.base.dump_ast(out)

    self.index.x = self.base.x + self.base.ancho
    self.index.y = self.y - (self.index.h_down + self.base.tam * 0.5)
    self.index.dump_ast(out)






class SubIndex(object):
  def __init__(self, base, index):
    initialize_atts(self)
    self.base = base
    self.index = index

  def name(self):
    return "SubIndex"

  def children(self):
    return [self.base, self.index]

  def recorrer(self):
    self.base.tam = self.tam
    self.base.recorrer()
    self.index.tam = self.tam * 0.7
    self.index.recorrer()

  def recorrer2(self):
    self.base.recorrer2()
    self.index.recorrer2()
    self.ancho = self.base.ancho + self.index.ancho
    # CHECK CHECK
    self.h_up = self.base.h_up
    self.h_down = self.base.h_down + self.index.altura * 0.7
    self.altura = self.h_up + self.h_down

  def dump_ast(self, out):
    self.base.x = self.x
    self.base.y = self.y
    self.base.dump_ast(out)

    self.index.x = self.base.x + self.base.ancho
    self.index.y = self.base.y + (self.index.h_up)
    self.index.dump_ast(out)




class SuperSubIndex(object):
  def __init__(self, base, super_index, sub_index):
    initialize_atts(self)
    self.base = base
    self.super_index = super_index
    self.sub_index = sub_index

  def name(self):
    return "SuperSubIndex"

  def children(self):
    return [self.base, self.super_index, self.sub_index]

  def recorrer(self):
    self.base.tam = self.tam
    self.base.recorrer()
    self.super_index.tam = self.tam * 0.7
    self.super_index.recorrer()
    self.sub_index.tam = self.tam * 0.7
    self.sub_index.recorrer()

  def recorrer2(self):
    self.base.recorrer2()
    self.super_index.recorrer2()
    self.sub_index.recorrer2()
    self.ancho = self.base.ancho + max(self.super_index.ancho, self.sub_index.ancho)
    # CHECK CHECK
    self.h_up = self.base.h_up + self.super_index.altura * 0.7
    self.h_down = self.base.h_down + self.sub_index.altura * 0.7
    self.altura = self.h_up + self.h_down

  def dump_ast(self, out):
    self.base.x = self.x
    self.base.y = self.y
    self.base.dump_ast(out)

    self.super_index.x = self.base.x + self.base.ancho
    self.super_index.y = self.base.y - (self.super_index.h_down + self.base.tam * 0.5)
    self.super_index.dump_ast(out)

    self.sub_index.x = self.base.x + self.base.ancho
    self.sub_index.y = self.base.y + (self.sub_index.h_up)
    self.sub_index.dump_ast(out)



class SubSuperIndex(object):
  def __init__(self, base, sub_index, super_index):
    initialize_atts(self)
    self.base = base
    self.sub_index = sub_index
    self.super_index = super_index

  def name(self):
    return "SubSuperIndex"

  def children(self):
    return [self.base, self.sub_index, self.super_index]

  def recorrer(self):
    self.base.tam = self.tam
    self.base.recorrer()
    self.sub_index.tam = self.tam * 0.7
    self.sub_index.recorrer()
    self.super_index.tam = self.tam * 0.7
    self.super_index.recorrer()

  def recorrer2(self):
    self.base.recorrer2()
    self.super_index.recorrer2()
    self.sub_index.recorrer2()
    self.ancho = self.base.ancho + max(self.super_index.ancho, self.sub_index.ancho)
    # CHECK CHECK
    self.h_up = self.base.h_up + self.super_index.altura * 0.7
    self.h_down = self.base.h_down + self.sub_index.altura * 0.7
    self.altura = self.h_up + self.h_down

  def dump_ast(self, out):
    self.base.x = self.x
    self.base.y = self.y
    self.base.dump_ast(out)

    self.super_index.x = self.base.x + self.base.ancho
    self.super_index.y = self.base.y - (self.super_index.h_down + self.base.tam * 0.5)
    self.super_index.dump_ast(out)

    self.sub_index.x = self.base.x + self.base.ancho
    self.sub_index.y = self.base.y + (self.sub_index.h_up)
    self.sub_index.dump_ast(out)



class Parenthesis(object):
  def __init__(self, content):
    initialize_atts(self)
    self.content = content

  def name(self):
    return "Parenthesis"

  def children(self):
    return [self.content]

  def recorrer(self):
    self.content.tam = self.tam
    self.content.recorrer()

  def recorrer2(self):
    self.content.recorrer2()
    self.ancho = self.content.ancho
    self.h_up = self.content.h_up
    self.h_down = self.content.h_down

  def dump_ast(self, out):
    self.content.x = self.x
    self.content.y = self.y
    out.append( make_open_paren(str(0), str(0), str(1), str(self.x - 0.45),str(self.y + self.h_up * 0.6),
                                str(1), str(self.tam * 1) ) )
    self.content.dump_ast(out)
    out.append( make_close_paren( str(0), str(0), str(1), str(self.x + self.ancho - 0.15),str(self.y + self.h_up * 0.6),
                                str(1), str(self.tam * 1)) )

class Id(object):
  def __init__(self, value):
    initialize_atts(self)
    self.value = value

  def name(self):
    return "ID"

  def children(self):
    return []

  def recorrer(self):
    return

  def recorrer2(self):
    self.ancho = self.tam * k2 # el ancho es 0.6 del tam del caracter
    self.h_up = 0.8 * self.tam
    self.h_down = 0.2 * self.tam
    self.altura = self.h_up + self.h_down

  def dump_ast(self, out):
    out.append( make_text(str(self.x), str(self.y), str(self.tam), str(self.value) ) )
