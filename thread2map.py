

from multiprocessing.dummy import Pool as ThreadPool

#from multiprocessing import Pool as ThreadPool

import urllib2

urls = [
  'http://www.baidu.com',
  'http://www.baidu.com',
  #'http://www.python.org',
  #'http://www.python.org/about/',
]

pool = ThreadPool(4)

results = pool.map(urllib2.urlopen, urls)   #并行处理

pool.close()
pool.join()

