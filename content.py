


import time
 
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
 
    def __enter__(self):
        self.start = time.time()
        return self
 
    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs
            
            
            
from timer import Timer
from redis import Redis
rdb = Redis()
 
with Timer() as t:
    rdb.lpush("foo", "bar")
print "=> elasped lpush: %s s" % t.secs
 
with Timer as t:
    rdb.lpop("foo")
print "=> elasped lpop: %s s" % t.secs
























###############################################
'''
粗粒度的计算时间

我们先来用个很快的方法来给我们的代码计时：使用unix的一个很好的功能 time。
1
2
3
4
5
	
$ time python yourprogram.py
 
real    0m1.028s
user    0m0.001s
sys     0m0.003s

关于这3个测量值的具体含义可以看这篇文章，但是简要的说就是：

    real：代表实际花费的时间
    user:：代表cpu花费在内核外的时间
    sys：代表cpu花费在内核以内的时间

通过把sys和user时间加起来可以获得cpu在你的程序上花费的时间。

如果sys和user加起来的时间比real时间要小很多，那么你可以猜想你的程序的大部分性能瓶颈应该是IO等待的问题。

 
用上下文管理器来细粒度的测量时间

我接下来要使用的技术就是让你的代码仪器化以让你获得细粒度的时间信息。这里是一个计时方法的代码片段：
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
	
import time
 
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
 
    def __enter__(self):
        self.start = time.time()
        return self
 
    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs

为了使用它，将你想要测量时间的代码用Python关键字with和Timer上下文管理器包起来。它会在你的代码运行的时候开始计时，并且在执行结束的完成计时。

下面是一个使用它的代码片段：
1
2
3
4
5
6
7
8
9
10
11
	
from timer import Timer
from redis import Redis
rdb = Redis()
 
with Timer() as t:
    rdb.lpush("foo", "bar")
print "=> elasped lpush: %s s" % t.secs
 
with Timer as t:
    rdb.lpop("foo")
print "=> elasped lpop: %s s" % t.secs

我会经常把这些计时器的输入记录进一个日志文件来让我知道程序的性能情况。













#任何定义了__enter__()和__exit__()方法的对象都可以用于上下文管理器。文件对象f是内置对象，所以f自动带有这两个特殊方法，不需要自定义。
'''
