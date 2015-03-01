#/usr/bin/python -O

print __debug__      #False



#/usr/bin/python

print __debug__     #Ture



assert x==y,"not equals"
#等价于
if __debug__ and not x==y:
  raise AssertionError("not equals")


#/usr/bin/python

if __debug__:
  gc.enable()
  gc.set_debug(gc.DEBUG_LEAK)
  ##########
  l=[]
  l.append(l)
  del l
  ###########
  gc.collect()
  for x in gc.garbage:
    s=str(x)
    if len(s)>80:s=s[:77]+'...'
    print type(x),"\n",s
    



##############################
#sys.exc_info()
#traceback.print_exc()
#traceback.extract_stack()


#sitecustomize.py
import os
def hinfo(type, value, tb):
  if hasattr(sys, 'ps1') or not (sys.stderr.isatty() and sys.stdin.isatty()) or issubclass(type, SyntaxError):
    '''交互模式、wutty设备、语法错误，默认处理'''
    sys.__excepthook__(type,value,tb)
  else:
    import traceback, pdb
    traceback.print_exception(type, value, tb)
    print
    pdb.pm()
sys.excepthook=hinfo
