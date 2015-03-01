
class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass
  def __setattr__(self, name, value):
    if name in self.__dict__:
      raise self.ConstError("Can't change const.%s" % name)
    if not name.isupper():
      raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
    self.__dict__[name] = value
    
import sys
sys.modules[__name__] = _const()  #使得对const模块的导入，得到的是_const实例对象


'''
使用：
import const                      #const is a const._const object
const.MY_CONSTANT=1               #一旦初始化，不能再次修改
print(const.MY_CONSTANT)
'''
