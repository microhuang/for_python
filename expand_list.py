def list_or_tuple(x):
    return isinstance(x, (list, tuple))

def flatten(sequence, to_expand=list_or_tuple):  
    for item in sequence:  
        if to_expand(item):  
            for subitem in flatten(item, to_expand):  
                yield subitem
        else:  
            yield item
            

#非递归版本：后进先出（LIFO）栈
def flatten(sequence, to_expand=list_or_tuple):  
    iterators = [ iter(sequence) ] 
    while iterators:
      for item in iterators[-1]:  #后进先出，遍历当前迭代器
        if to_expand(item):  #如果需要进一步展开
            iterators.append(iter(item))  #将子序列的迭代器压入“栈”顶
            break
        else:  
            yield item  #如果不需要展开，则直接返回
      else: #当前迭代器已经遍历完，返回上层
        iterators.pop()  #从“栈”顶删除已经处理过的序列迭代器
 
            
for x in flatten([1,2,[3,[],4,[5,6],7,[8,],],9]):
    print x
    
    
