#!/usr/bin/env python


import select
#导入select模块

BLKSIZE=8192

def readwrite(fromfd,tofd):
    readbuf = fromfd.read(BLKSIZE)
    if readbuf:
        tofd.write(readbuf)
        tofd.flush()
    return len(readbuf)

def copy2file(fromfd1,tofd1,fromfd2,tofd2):
        ''' using select to choice fds'''
    totalbytes=0
        if not (fromfd1 or fromfd2 or tofd1 or tofd2) :
#检查所有文件描述符是否合法
                return 0
    while True:
#开始利用select对输入所有输入的文件描述符进行监视
        rs,ws,es = select.select([fromfd1,fromfd2],[],[])
        for r in rs:

            if r is fromfd1:
#当第一个文件描述符可读时，读入数据
                bytesread = readwrite(fromfd1,tofd1)            
                totalbytes += bytesread
            if r is fromfd2:
                bytesread = readwrite(fromfd2,tofd2)
                totalbytes += bytesread
        if (bytesread <= 0):
            break
    return totalbytes
def main():
    
    fromfd1 = open("/etc/fstab","r")
    fromfd2 = open("/etc/passwd","r")

    tofd1 = open("/root/fstab","w+")
    tofd2 = open("/root/passwd","w+")

    totalbytes = copy2file(fromfd1,tofd1,fromfd2,tofd2)
    
    print "Number of bytes copied %d\n" % totalbytes
    return 0
    


if __name__=="__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#!/usr/bin/env python


import select
BLKSIZE=8192

def readwrite(fromfd,tofd):
    readbuf = fromfd.read(BLKSIZE)
    if readbuf:
        tofd.write(readbuf)
        tofd.flush()
    return len(readbuf)

def copyPoll(fromfd1,tofd1,fromfd2,tofd2):
   #定义需要监听的事件
    READ_ONLY = (select.POLLIN |
             select.POLLPRI |
            select.POLLHUP |
            select.POLLERR )
    totalbytes=0
    
        if not (fromfd1 or fromfd2 or tofd1 or tofd2) :
        return 0
    fd_dict = {fromfd1.fileno():fromfd1,fromfd2.fileno():fromfd2}
    #创建poll对象p
    p=select.poll()
    #利用poll对象p对需要监视的文件描述符进行注册
    p.register(fromfd1,READ_ONLY)
    p.register(fromfd2,READ_ONLY)
    while True:
  #轮询已经注册的文件描述符是否已经准备好
        result = p.poll()
        if len(result) != 0:
            for fd,events in result:
                if fd_dict[fd] is fromfd1:
                    if events & (select.POLLIN|select.POLLPRI):
                        bytesread = readwrite(fromfd1,tofd1)
                        totalbytes+=bytesread
    
                    elif events & (select.POLLERR):
                        p.unregister(fd_dict[fd])
            
                if fd_dict[fd] is fromfd2:
                    if events & (select.POLLIN|select.POLLPRI):
                        bytesread = readwrite(fromfd2,tofd2)
                        totalbytes+=bytesread
                    elif events & (select.POLLERR):
                        p.unregister(fd_dict[fd])
        if bytesread <= 0:    
            break
    return totalbytes
    
def main():
    
    fromfd1 = open("/etc/fstab","r")
    fromfd2 = open("/root/VMwareTools-8.8.1-528969.tar.gz","r")

    tofd1 = open("/root/fstab","w+")
    tofd2 = open("/var/passwd","w+")

    totalbytes = copyPoll(fromfd1,tofd1,fromfd2,tofd2)
    print "Number of bytes copied %d\n" % totalbytes
    return 0
    


if __name__=="__main__":
    main()
