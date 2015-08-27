# -*- coding: utf-8 -*-
__author__ = 'florije'

import json
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
import tcelery
import nothing
from nothing import add


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        print "CALLING get()"
        xxx = 10
        yyy = 2
        nothing.add.apply_async(args=[xxx, yyy])




application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(10001)
    tornado.ioloop.IOLoop.instance().start()