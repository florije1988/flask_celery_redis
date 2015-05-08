# -*- coding: utf-8 -*-
__author__ = 'florije'

# import tornado.ioloop
# import tornado.web
#
#
# class MainHandler(tornado.web.RequestHandler):
# def get(self):
#         self.write("Hello, world")
#
#
# application = tornado.web.Application([
#     (r"/", MainHandler),
# ])
#
# if __name__ == "__main__":
#     application.listen(8888)
#     tornado.ioloop.IOLoop.instance().start()

from tornado import gen
from tornado import ioloop
from tornado.web import asynchronous, RequestHandler, Application

import tasks

import tcelery

tcelery.setup_nonblocking_producer()


class AsyncHandler(RequestHandler):
    @asynchronous
    def get(self):
        tasks.sleep.apply_async(args=[3], callback=self.on_result)

    def on_result(self, response):
        self.write(str(response.result))
        self.finish()


class GenAsyncHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        response = yield gen.Task(tasks.sleep.apply_async, args=[3])
        self.write(str(response.result))
        self.finish()


class GenMultipleAsyncHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        r1, r2 = yield [gen.Task(tasks.sleep.apply_async, args=[2]),
                        gen.Task(tasks.add.apply_async, args=[1, 2])]
        self.write(str(r1.result))
        self.write(str(r2.result))
        self.finish()


application = Application([
    (r"/async-sleep", AsyncHandler),
    (r"/gen-async-sleep", GenAsyncHandler),
    (r"/gen-async-sleep-add", GenMultipleAsyncHandler),
])

if __name__ == "__main__":
    application.listen(8887)
    ioloop.IOLoop.instance().start()