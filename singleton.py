import threading
class s():
    i=None
    mutex=threading.Lock()
    @staticmethod
    def g():
        if(s.i==None):
            s.mutex.acquire()
            s.i=s()
            s.mutex.release()
        return s.i
        
c1=s.g()
c2=s.g()




class Singleton(object):
  def __new__(cls, *args, **kwargs):
    if '_inst' not in vars(cls):
      cls._inst=super(Singleton, cls).__new__(cls, *args, **kwargs)
      #cls._inst=object.__new__(cls, *args, **kwargs)
    return cls._inst


class SingleSpam(Singleton):
  pass

c1=SingleSpam()
c2=SingleSpam()





class Borg(object):
    _shared_state={}
    def __new__(cls, *a, **k):
        obj=object.__new__(cls, *a, **k)
        #obj=super(Borg, cls).__new__(cls, *a, **k)
        obj.__dict__=cls._shared_state
        return obj

class Example(Borg):
    name=None
    def __init__(self, name=None):
            if name is not None: self.name=name
    def __str__(self): return 'name->%s' % self.name

a=Example('Lara')
b=Example()
print a,b
        



class froober(object):
    def __init__(self):
        pass
    
    
froober=froober()
