import signal
 
# An implementation of cooperative multithreading using generators
# that handles signals; by Brian O. Bush
 
# credit: based off an article by David Mertz
# http://gnosis.cx/publish/programming/charming_python_b7.txt
 
def empty(name):
    """ This is an empty task. """
    while True:
        print "<empty process>", name
        yield None

def terminating(name, maxn):
    for i in xrange(maxn):
        print "here %s, %s out of %s" % (name, i, maxn)
        yield None
    print "Done with %s, bailing out after %s times" % (name, maxn)

def delay(duration=0.8):
    import time
    while True:
        print "<sleep %d>" % duration
        time.sleep(duration)
        yield None

class GenericScheduler(object):
    def __init__(self, threads, stop_asap=False):
        signal.signal(signal.SIGINT, self.shutdownHandler)
        self.shutdownRequest = False
        self.threads = threads
        # add some "processes"
        #self.threads.append(delay(1))
        #self.threads.append(delay(2))
        #self.threads.append(empty())
        self.stop_asap=stop_asap
    def shutdownHandler(self, n, frame):
        """ Initiate a request to shutdown cleanly on SIGINT."""
        print "Request to shut down."
        self.shutdownRequest = True       
    def scheduler(self):
        def noop():
            while True: yield None
        n=len(self.threads)
        while True:
            for i, thread in enumerate(self.threads):
                try: thread.next()
                except StopIteration:
                    if self.stop_asap: return
                    n-=1
                    if n==0: return
                    self.threads[i]=noop()
                if self.shutdownRequest:
                    return
 
if __name__== "__main__":
    s = GenericScheduler([empty('boo'), delay(), empty('boo'), terminating('fie',5), delay(0.5), ], stop_asap=True)
    s.scheduler()
    s = GenericScheduler([empty('boo'), delay(), empty('boo'), terminating('fie',5), delay(0.5), ], stop_asap=True)
    s.scheduler()
