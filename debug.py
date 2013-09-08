#/usr/bin/python -O

print __debug__      #False



#/usr/bin/python

print __debug__     #Ture


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
    
