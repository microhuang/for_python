队列方式

```
jobs = multiprocessing.JoinableQueue() #任务队列
results = multiprocessing.Queue() #结果队列
canceld = False
for _ in range(multiprocessing.cpu_count()):
  process = multiprocessing.Process(target=worker,args=(jobs,results)) #创建wrok
  process.daemon = True
  process.start()
for _  in range(10):
  jobs.put(_)    #添加任务
try:
  jobs.join()    #直到队列处理完成
except KeyboardInterrupt:
  canceld = True
while not results.empty():
  result = results.get_nowait()  #获取结果
  
def work(jobs,results):
  while True:
    try:
        x = jobs.get() #获取任务
        result = foo()
        results.put(result) #保存结果
    finally:
      jobs.task_done()
```

进程池

```
futures
```
