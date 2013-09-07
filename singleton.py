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
    return cls._inst


class SingleSpam(Singleton):
  pass

c1=SingleSpam()
c2=SingleSpam()
