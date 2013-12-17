import multitask
import time
def f1():
     for i in range(3):
             print 'f1'
             yield
 

def f2():
     for i in range(3):
             print 'f2'
             yield
 

multitask.add(f1())
multitask.add(f2())
multitask.run()
