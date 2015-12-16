k1 = 0.6
k2 = 0.6

def initialize_atts(obj):
  obj.tam = 1
  obj.ancho = 0
  obj.x = 0
  obj.y = 0
  obj.h1 = 0
  obj.h2 = 0

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
    self.sub_index.recorrer2()
    self.super_index.recorrer2()
    self.ancho = self.base.ancho + max(self.super_index.ancho, self.sub_index.ancho)

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
