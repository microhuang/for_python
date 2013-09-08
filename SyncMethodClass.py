import inspect

def wrap_callable(any_callable, before, after):
    """
    Wrap any callable with before/after calls.

    From the Python Cookbook. Modified to support C{None} for
    C{before} or C{after}.

    @copyright: O'Reilly Media

    @param any_callable: The function to decorate.
    @type any_callable: function
    
    @param before: The pre-processing procedure. If this is C{None}, then no pre-processing will be done.
    @type before: function
    
    @param after: The post-processing procedure. If this is C{None}, then no post-processing will be done.
    @type after: function
    """
    def _wrapped(*a, **kw):
        if before is not None:
            before( )
        try:
            return any_callable(*a, **kw)
        finally:
            if after is not None:
                after( )
    # In 2.4, only: _wrapped.__name__ = any_callable.__name__
    return _wrapped

class GenericWrapper( object ):
    """
    Wrap all of an object's methods with before/after calls. This is
    like a decorator for objects.

    From the I{Python Cookbook}.

    @copyright: O'Reilly Media
    """
    def __init__(self, obj, before, after, ignore=( )):
        # we must set into __dict__ directly to bypass __setattr__; so,
        # we need to reproduce the name-mangling for double-underscores
        clasname = 'GenericWrapper'
        self.__dict__['_%s__methods' % clasname] = {  }
        self.__dict__['_%s__obj' % clasname] = obj
        for name, method in inspect.getmembers(obj, inspect.ismethod):
            if name not in ignore and method not in ignore:
                self.__methods[name] = wrap_callable(method, before, after)
    def __getattr__(self, name):
        try:
            return self.__methods[name]
        except KeyError:
            return getattr(self.__obj, name)
    def __setattr__(self, name, value):
        setattr(self.__obj, name, value)

class SynchronizedObject(GenericWrapper):
    ''' wrap an object and all of its methods with synchronization '''
    def __init__(self, obj, ignore=(), lock=None):
        if lock is None:
            import threading
            lock = threading.RLock()
        GenericWrapper.__init__(self, obj, lock.acquire, lock.release, ignore)


if __name__ == '__main__':
    import threading
    import time
    class Dummy(object):
        def foo(self):
            print "foo fun"
            time.sleep(10)
        def bar(self):
            print "bar fun"
        def baaz(self):
            print "baaz fun"
    tw = SynchronizedObject(Dummy(),ignore=['baaz'])
    threading.Thread(target=tw.foo).start()
    time.sleep(1)
    threading.Thread(target=tw.bar).start()
    time.sleep(1)
    threading.Thread(target=tw.baaz).start()
