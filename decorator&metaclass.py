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

def pre_str(pre=''):
    # old decorator
    def decorator(F):
        def new_F(a, b):
            print(pre + "input", a, b)
            return F(a, b)
        return new_F
    return decorator

# get square sum
@pre_str('^_^')
def square_sum(a, b):
    return a**2 + b**2
