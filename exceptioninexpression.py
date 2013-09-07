def throws(t,f,*a,**k):
  try:
    f(*a,**k)
  except:
    return True
  else:
    return False
    
    

data=[float(line) for line in open(some_file) if not throws(ValueError,float,line)]


def returns(t, f, *a, **k):
  try:
    return [ f(*a, **k) ]
  except t:
    return []
    
    

data=[x for line in open(some_file) for x in returns(ValueError, float, line)]
