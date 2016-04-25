先看一组对比数据：

Flask（自带web服务）

```
ab -n 1000 -c 20 'http://127.0.0.1:5000/api/guess?model=mailoshopload&utype=1&uid=123456&debug=1'

Time per request:       72.537 [ms] (mean)


Gunicorn+gevent

ab -n 1000 -c 20 'http://127.0.0.1:5001/api/guess?model=mailoshopload&utype=1&uid=123456&debug=1'

Time per request:       38.336 [ms] (mean)
```

代码啥的，什么不动，换了个web服务，性能提升一倍，Why？

都知道flask依赖werkzeug，那我们来看看，不借用flask，自己怎样写app。

```
1. import os  
2. import redis  
3. import urlparse  
4. from werkzeug.wrappers import Request, Response  
5. from werkzeug.routing import Map, Rule  
6. from werkzeug.exceptions import HTTPException, NotFound  
7. from werkzeug.wsgi import SharedDataMiddleware  
8. from werkzeug.utils import redirect  
9. from jinja2 import Environment, FileSystemLoader  
10. 
11. class Shortly(object):  
12.     def __init__(self, config):  
13.         self.redis = redis.Redis(config[‘redis_host’], config[‘redis_port’])  
14.   
15.     def dispatch_request(self, request):  
16.         return Response(‘Hello World!’)  
17.   
18.     def wsgi_app(self, environ, start_response):  
19.         request =  Request(environ)  
20.         response = self.dispatch_request(request)  
21.         return response(environ, start_response)  
22.   
23.     def __call__(self, environ, start_response):  
24.         return self.wsgi_app(environ, start_response)  
25.   
26. def create_app(redis_host=‘localhost’, redis_port=6379, with_static=True):  
27.     app = Shortly({  
28.         ‘redis_host’:   redis_host,  
29.         ‘redis_port’:   redis_port  
30.     })  
31.     if with_static:  
32.         app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {  
33.             ‘/static’:  os.path.join(os.path.dirname(__file__), ‘static’)  
34.         })  
35.     return app
36. 
37. if __name__ == ‘__main__’:  
38.     from werkzeug.serving import run_simple  
39.     app = create_app()  
40.     run_simple(‘127.0.0.1’, 5000, app, use_debugger=True, use_reloader=True)       #werkzeug
41.  
42. if __name__ != '__main__':
43.     app = create_app()                             #等 gunicorn + gevent 启动
```

以上app实现简明扼要，根据WSGI规范要求：
①你要定义一个入口函数，所有请求都将转到该入口函数来处理。
②入口函数必须接收env和start_response这两个参数。对于类而言，我们需要定义魔术方法__call__使得这个类可以作为WSGI入口。

而run_simple则帮我们做了简单的socket服务工作，其中run_simple -> make_server -> ThreadedWSGIServer | ForkingWSGIServer | 
BaseWSGIServer，它们都通过socketserver.ThreadingMixIn处理多任务，通过HTTPServer处理http协议。在此，可以看到内置（werkzeug）服务实际上通过标准的多线程和多进程两种方式处理http请求与响应。没有协程、没有异步I/O，神马也没有。。。

使用gunicorn替代run_simple则允许我们更简单的借用gevent、tornado等广泛的异步并行框架大大提供并发处理能力。
