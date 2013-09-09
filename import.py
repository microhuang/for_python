import new
def importCode(code, name, add_to_sys_modules=False):
  module=new.module(name)
  if add_to_sys_modules:
    import sys
    sys.modules[name]=module
  exec code in module.__dict__
  return module
  
  
  
#import foo
if 'foo' in sys.modules:
  foo=sys.modules['foo']
else:
  foofile=open("/path/to/foo.py")
  foo=importCode(foofile,"foo",1)
