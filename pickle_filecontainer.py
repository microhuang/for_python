import cPickle
class PrettyClever(object):
    def __init__(self, *stuff):
            self.stuff=stuff
    def p(self, x): print "Hello,", x
    def __getstate__(self):
            def normalize(x):
                    if isinstance(x, file):
                            return 1, (x.name, x.mode, x.tell())
                    return 0, x
            return [normalize(x) for x in self.stuff]
    def __setstate__(self,stuff):
            def reconstruct(x):
                    if x[0]==0:
                            return x[1]
                    name,mode,offs=x[1]
                    openfile=open(name,mode)
                    openfile.seek(offs)
                    return openfile
            self.stuff=tuple([reconstruct(x) for x in stuff])

anInstance=PrettyClever(1,2,3)

saved=cPickle.dumps(anInstance)
reloaded=cPickle.loads(saved)
assert anInstance.stuff==reloaded.stuff
reloaded.p("world")

anotherInstance=PrettyClever(1,2,open('tags.xml','w'))

saved=cPickle.dumps(anotherInstance)
reloaded=cPickle.loads(saved)
assert anotherInstance.stuff==reloaded.stuff
assert anotherInstance.stuff[0:2]==reloaded.stuff[0:2]
assert anotherInstance.stuff[2]==reloaded.stuff[2]
