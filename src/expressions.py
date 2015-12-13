class Divide(object):

  def __init__(self, left, right):
    self.left = left
    self.right = right

  def name(self):
    return "Divide"

  def children(self):
    return [self.left, self.right]


class Concat(object):

  def __init__(self, left, right):
    self.left = left
    self.right = right

  def name(self):
    return "Concat"

  def children(self):
    return [self.left, self.right]

class SuperIndex(object):

  def __init__(self, base, index):
    self.base = base
    self.index = index

  def name(self):
    return "SuperIndex"

  def children(self):
    return [self.base, self.index]


class SubIndex(object):

  def __init__(self, base, index):
    self.base = base
    self.index = index

  def name(self):
    return "SubIndex"

  def children(self):
    return [self.base, self.index]

class SuperSubIndex(object):

  def __init__(self, base, super_index, sub_index):
    self.base = base
    self.super_index = super_index
    self.sub_index = sub_index

  def name(self):
    return "SuperSubIndex"

  def children(self):
    return [self.base, self.super_index, self.sub_index]


class SubSuperIndex(object):

  def __init__(self, base, sub_index, super_index):
    self.base = base
    self.sub_index = sub_index
    self.super_index = super_index

  def name(self):
    return "SubSuperIndex"

  def children(self):
    return [self.base, self.sub_index, self.super_index]

class Parenthesis(object):

  def __init__(self, content):
    self.content = content

  def name(self):
    return "Parenthesis"

  def children(self):
    return [self.content]


class Id(object):

  def __init__(self, value):
    self.value = value

  def name(self):
    return "ID"

  def children(self):
    return []
