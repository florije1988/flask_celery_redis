# -*- coding: utf-8 -*-
__author__ = 'florije'

import tornado.ioloop
from tornado import gen, web
import tcelery
import tasks

"""
celery -A tasks worker --loglevel=info
python tasks.py worker --loglevel=info
"""

# tcelery.setup_nonblocking_producer()


class AsyncHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        # tasks.echo.apply_async(args=['Hello world!'], callback=self.on_result)
        tasks.add.apply_async(args=[1, 2], callback=self.on_result)
        # self.write('success')
        # self.finish()

    def on_result(self, response):
        self.write(str(response.result))
        self.finish()


class GenAsyncHandler(web.RequestHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        response = yield gen.Task(tasks.sleep.apply_async, args=[3])
        self.write(str(response.result))
        self.finish()


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")


application = web.Application([
    (r"/", MainHandler),
    (r"/async", AsyncHandler),
    (r"/gen", GenAsyncHandler),
])

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()