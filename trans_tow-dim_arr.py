arr=[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]

print [[r[col] for r in arr] for col in range(len(arr[0]))]

print map(list,zip(*arr))

import itertools
print map(list,itertools.izip(*arr))  #生成器方式
