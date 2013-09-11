import itertools
def par_loop(padding_item, *sequences):
    iterators = map(iter, sequences)
    num_remaining = len(iterators)
    result = [padding_item] * num_remaining
    while num_remaining:
        for i, it in enumerate(iterators):
            try: 
                 result[i] = it.next()
            except StopIteration:
                 iterators[i] = itertools.repeat(padding_item)
                 num_remaining -= 1
                 result[i] = padding_item
        if num_remaining:
            yield tuple(result)

print map(''.join, par_loop('x', 'foo', 'zapper', 'ui'))


a=[1,2,3]
b=[1,2,3,4,5,]


for x,y in map(None,a,b):
    print x,y

for x,y in par_loop(None,a,b):
    print x,y









import itertools
def par_two(a, b, padding_item=None):
    a, b = iter(a), iter(b)
    # first, deal with both iterables via izip until one is exhausted:
    for x in itertools.izip(a, b):
        yield x
    # only one of the following two loops, at most, will execute, since
    # either a or b (or both!) are exhausted at this point:
    for x in a:
        yield x, padding_item
    for x in b:
        yield padding_item, x

for x,y in par_two(a,b,None):
    print x,y
