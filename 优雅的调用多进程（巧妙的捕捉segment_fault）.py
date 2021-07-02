# 巧妙的捕捉segment fault
#
# 应用场景：在模型等一些需要多进程并行处理的时候，我们之前的使用方式是通过类似：result = pool.map(func , ....)，的方式把任务func叫给子进程处理，
# 此做法导致：子进程运行func的过程中，如果发生了segment fault等一些操作系统层面的错误，则调用方主进程一直等待子进程回复而不得，对于主进程而言，则看起来假死了
#
# 最佳实践：建议所有pool.map调用均按下列范式，以pool.apply_async替代

from functools import partial
from multiprocessing import Pool, Manager
from multiprocessing.context import TimeoutError

# 模拟业务
def func(proc_dict, proc_id, *args):
    import time
    import os
    # 业务方务必主动告知自身PID
    proc_dict[proc_id] = os.getpid()
    # ......
    if proc_id=='a':
        # 模拟 segment fault，此错误不能被try...except...
        try:
            import ctypes
            ctypes.string_at(0)
        except: # 无效，不能捕捉操作系统级错误
            pass
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
    if n+1>m and m>1:
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
        # 传统使用方式
        # result = pool.map(f, ('a','b','c'))
        # 最佳实践
        for proc in ('a', 'b', 'c'):
            res = pool.apply_async(func, (proc_dict, proc, '业务传参'))
            ret[proc] = res
        # result = []
        for proc in ret:
            try:
                timeout = 3
                # result.append(proc_result(ret[proc], proc, proc_dict, timeout, m=3))
                print('result: ', proc_result(ret[proc], proc, proc_dict, timeout, m=3))
            except (ProcessLookupError, OSError) as err:
                # segment fault 将被这里捕捉到
                print('进程(%s)已经结束了，可能是操作系统强制结束进程，可以在这里重试。。。' % (proc_dict[proc]))
                # raise err
            except Exception as err:
                if err.__str__().startswith("code:666,"):
                    # 逻辑上的假死将在这里捕捉到
                    print('进程长时间无结果，请检查！')
                    # raise err
                else:
                    # 其他错误在这里捕捉到了
                    print('其他错误')
                    # raise err
