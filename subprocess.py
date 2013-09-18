import subprocess

subp=subprocess.Popen('command', shell=True, stdout=subprocess.PIPE)
print subp.pid
print subp.wait()
print subp.returncode
print subp.stdout.readlines()


#http://docs.python.org/2/library/subprocess.html#module-subprocess
