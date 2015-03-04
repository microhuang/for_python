#测试驱动

'''
1、完成整体代码
def my_avg(x):
  pass
'''

'''
2、写测试用例
import unittest
from my_avg import my_avg
class TestAvg(unittest.TestCase):
  def test_int(self):
    print("test average of integers:"
    self.assertEqual(my_avg([0,1,2]),1)
  def test_float(self):
    print("test average of float:"
    self.assertEqual(my_avg([1.2,2.5,0.8]),1.5)
  def test_empty(self):
    print("test empty input:"
    self.assertFalse(my_avg([]),False)
  def test_mix(self):
    print("test with mix input:"
    self.assertEqual(my_avg([-1,3,7]),3)
  def test_invalid(self):
    print("test with invalid input:"
    self.assertRaises(TypeError,my_avg,[-1,3,[1,2,3]])
if __name__ == '__main__':
  unittest.main()
'''

'''
3、完善代码
def my_avg(x):
  if len(*x)<=0:
    print("you need input at least on number")
    return false
  sum=0
  try:
    for i in x:
      sum += i
  except(TypeError):
    raise TypeError("your input is not value with unsupported type")
  return sum/len(x)
4、重构代码
def my_avg(*x):
  if len(*x)<=0:
    print("you need input at least on number")
    return false
  try:
    return sum(*x)/len(*x)
  except(TypeError):
    raise TypeError("your input is not value with unsupported type")
'''
