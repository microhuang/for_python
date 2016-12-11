import socks
import socket
from urllib.request import urlopen

#先开启tor
socks.set_default_proxy(socks.SOCKS5,"localhost",9150)
socket.socket = socks.socksocket

#查看tor代理后的暴露IP
print(urlopen("http://icanhazip.com").read())
