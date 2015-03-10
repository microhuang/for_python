#decorator

@wrapper       ======        func=wrapper(func)



#如果说类是对象实例的模板，那么元类就是类的模板。




# get square sum

def square_sum(a, b):
    return a**2 + b**2

# get square diff
def square_diff(a, b):
    return a**2 - b**2
    
   
# 期望改为下面的行为 
    

# get square sum
def square_sum(a, b):
    print("intput:", a, b)
    return a**2 + b**2

# get square diff
def square_diff(a, b):
    print("input", a, b)
    return a**2 - b**2
    
    
    
#使用装饰器，不修改原函数的情况下更改功能



def decorator(F):
    @functools.wraps(F)
    def new_F(a, b):
        print("input", a, b)
        return F(a, b)
    return new_F

# get square sum
@decorator
def square_sum(a, b):
    return a**2 + b**2

# get square diff
@decorator
def square_diff(a, b):
    return a**2 - b**2

print(square_sum(3, 4))
print(square_diff(3, 4))



#给装饰器增加参数支持



# a new wrapper layer

def pre_str(pre=None):
    # old decorator
    def decorator(F):
        @functools.wraps(F)
        def new_F(a, b):
            print(pre + "input", a, b)
            return F(a, b)
        return new_F
    return decorator

# get square sum
@pre_str('^_^')
def square_sum(a, b):
    return a**2 + b**2
    
    
# demo

def mean(frist, second, *rest):
    numbers = (first, second) + rest
    return sum(numbers)/len(numbers)
    
    
mean = float_args_and_return(mean)


def float_args_and_return(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        args = [float(arg) for arg in args]
        return float(function(*args, **kwargs))
    return wrapper
    
    
def statically_typed(*types, return_type=None):
    def decorator(function):
        @functools.wraps(function):
        def wrapper(*args, *kwargs):
            if len(args)>len(types):
                raise ValueError("too many arguments")
            elif len(args)<len(types):
                raise ValueError("too few arguments")
            for i, (arg, type_) in enumerate(zip(args, types)):
                if not isinstance(arg, type_):
                    raise ValueError("argument {} must be of type {}".format(i, type_.__name__))
            result = function(*args, **kwargs)
            if (return_type is not None and not isinstance(result, return_type)):
                raise ValueError("return value must be of type {}".format(return_type.__name))
            return result
        return wrapper
    return decorator
