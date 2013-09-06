import time
import sched

s = sched.scheduler(time.time,time.sleep)

def task(para):
  print(para)
  
def s(inc,para):
  ss.enter(inc,0,p,(inc,para))
  task(para)
  
e1=s.enter(10,2,p,(10,"test"))
s.run()
