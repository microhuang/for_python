#!/bin/python2.7
#require tornado

import tornado.web
import tornado.ioloop
import tornado.websocket

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        SocketHandler.clients.add(self)
        self.write_message('Welcome to WebSocket')

    def on_close(self):
        SocketHandler.clients.remove(self)

class Index(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body>Hello, world!')

if __name__ == '__main__':
    app = tornado.web.Application([
        ('/', Index),
        ('/soc',SocketHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


#js
# new WebSocket('ws://192.168.13.203:8000/soc');         #403
