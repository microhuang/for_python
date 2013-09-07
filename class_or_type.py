
class Somebase(object):  #object masted be new style class
  pass

class Someclass(Somebase):
  __metaclass__=type
  x=23
  

Someclass=type('Someclass', (Somebase, ), {'x':23})
