import subprocess

subp=subprocess.Popen('command', shell=True, stdout=subprocess.PIPE)

#注意管道缓冲区满的问题 python -u ---- unbuffer

print subp.pid

c=subp.stdout.readline()
while c:
  print c
  c=subp.stdout.readline()   #注意客户程序”换行“要求，read()按长度读时考虑内容打乱的问题。
  
subp.wait()
print subp.returncode


#http://docs.python.org/2/library/subprocess.html#module-subprocess




print subp.pid

while subp.poll()==None:
  c=subp.stdout.readline()
  print c

print subp.returncode


#注意wait()和poll()的用法区别









#select poll epoll 管道





import subprocess
import select  
import time  
import signal  
import os  

cmd="python -u /tmp/produce.py"
cmd="php /tmp/test.php"
timeout = 60
pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell = True)
print time.time()

while 1:
    while_begin = time.time()
    print 'timeout',timeout
    fs = select.select([pro.stdout], [], [], timeout)
    if pro.stdout in fs[0]:
            tmp = pro.stdout.read()
            print 'read', tmp
            if not tmp:
                    print 'end'
                    print time.time() 
                    break
    else:
            print 'outoftime'
            print os.kill(pro.pid, signal.SIGKILL),
            break
    timeout = timeout - (time.time() - while_begin)

print 'end'
