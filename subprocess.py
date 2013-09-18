import subprocess

subp=subprocess.Popen('command', shell=True, stdout=subprocess.PIPE)

#注意管道缓冲区满的问题 python -u ---- unbuffer

print subp.pid

c=subp.stdout.readline()
while c:
  print c
  c=subp.stdout.readline()
  
subp.wait()
print subp.returncode


#http://docs.python.org/2/library/subprocess.html#module-subprocess




print subp.pid

while subp.poll()==None:
  c=subp.stdout.readline()
  print c

print subp.returncode


#注意wait()和poll()的用法区别
