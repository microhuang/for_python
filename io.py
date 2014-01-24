#!/usr/bin/env python
#coding=utf-8
import os
import fcntl
import select, sys, subprocess

vmstat_pipe = subprocess.Popen('netstat', shell=True, bufsize=1024, 
        stdout=subprocess.PIPE).stdout
iostat_pipe = subprocess.Popen('top', shell=True, bufsize=1024, 
        stdout=subprocess.PIPE).stdout
        
'''
#noblock
fl = fcntl.fcntl(vmstat_pipe.fileno(), fcntl.F_GETFL)
fcntl.fcntl(vmstat_pipe.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
fl = fcntl.fcntl(iostat_pipe.fileno(), fcntl.F_GETFL)
fcntl.fcntl(iostat_pipe.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
'''

#select
while 1:
    infds,outfds,errfds = select.select([vmstat_pipe,iostat_pipe],[],[],5000)
    if len(infds) != 0:
        for m in infds:
            msg = m.readline()
            print "Get ", msg, "from pipe", m
            
'''
#poll
pipe_dict = {vmstat_pipe.fileno():vmstat_pipe, iostat_pipe.fileno():iostat_pipe}
p = select.poll()
p.register(vmstat_pipe, select.POLLIN|select.POLLERR|select.POLLHUP)
p.register(iostat_pipe, select.POLLIN|select.POLLERR|select.POLLHUP)
while 1:
    result = p.poll(5000)
    if len(result) != 0:
        for m in result:
            if m[1] & select.POLLIN:
                print "Get", pipe_dict[m[0]].readline(), "from pipe", m[0]
                
#epoll
pipe_dict = {vmstat_pipe.fileno():vmstat_pipe, iostat_pipe.fileno():iostat_pipe}
p = select.epoll()
p.register(vmstat_pipe, select.POLLIN|select.POLLERR|select.POLLHUP)
p.register(iostat_pipe, select.POLLIN|select.POLLERR|select.POLLHUP)
while 1:
    result = p.poll(5000)
    if len(result) != 0:
        for m in result:
            if m[1] & select.POLLIN:
                print "Get", pipe_dict[m[0]].readline(), "from pipe", m[0]
'''
