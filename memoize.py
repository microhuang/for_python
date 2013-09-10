
def memoize(function):
  memo = {}
  def wrapper(*args, **k_args):
    if k_args:
      return function(*args, **k_args)
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper

@memoize
def fib(n):
   if n in (0, 1):
      return n
   return fib(n-1) + fib(n-2)

#fib=memoize(fib)         #  ===> @memoize

fib(10)
