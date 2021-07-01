# 巧妙的捕捉segment fault

from functools import partial
from multiprocessing import Pool, Manager
from multiprocessing.context import TimeoutError

# 模拟业务
def f(proc_dict, proc_id, *args):
  import time
  import os
  proc_dict[proc_id] = os.getpid()
  # ......
  if proc_id=='a':
    # 模拟 segment fault
    import ctypes
    ctypes.string_at(0)
    return '意思一下'
  elif proc_id=='b':
    # 模拟超时
    time.sleep(6)
    return '意思两下'
  else:
    # 模拟其他
    return '意思三下'
  
# proc: ApplyResult
# proc_id: {proc_id:pid}
# proc_dict: {proc_id:pid}
# timeout: 
# m: max call
# n: current call
def proc_result(proc, proc_id, proc_dict, timeout, m=2, n=1):
  if n+1>m:
    title = ''
    if proc_dict.get(proc_id):
      title = proc_dict.get(proc_id)
    raise Exception("code:666,等待(%s)轮，依然无运行结果，请检查进程(%s)是否异常" % (m, title))
  ret = None
  try:
    ret = proc.get(timeout)
  except TimeoutError as err:
    try:
      import os
      os.kill(proc_dict[proc_id], 0)
      ret = proc_result(proc, proc_id, proc_dict, timeout, m=m, n=n+1)
    except (ProcessLookupError, OSError) as err:
      raise err
  return ret

if __name__ == '__main__':
  ret = {}
  with Pool(4) as pool:
    manager = Manager()
    proc_dict = manager.dict()
    for proc in ('a', 'b', 'c'):
      res = pool.apply_async(f, (proc_dict, proc, '业务传参'))
      ret[proc] = res
    for proc in ret:
      try:
        timeout = 2
        print('result: ', proc_result(ret[proc], proc, proc_dict, timeout))
      except (ProcessLookupError, OSError) as err:
        print('进程(%s)已经结束了，可能是操作系统强制结束进程，可以在这里重试。。。' % (proc_dict[proc]))
      except Exception as err:
          if err.__str__().startswith("code:666,"):
              print('进程长时间无结果，请检查！')
              raise err
          else:
              raise err
