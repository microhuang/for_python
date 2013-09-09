def curry(f, *a, **kw):
    def curried(*more_a, **more_kw):
        return f(*(a+more_a), **dict(kw.items()+more_kw.items()))
    return curried

foo2 = curry(foo, b=2)
foo2(a=1, c=3)
#=>6




from functools import partial
def foo(a,b,c):
    return a+b+c

foo2 = partial(foo, b=2)
foo2(a=1, c=3)
#=>6
