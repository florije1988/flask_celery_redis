# -*- coding: utf-8 -*-
__author__ = 'florije'

from time import sleep
from celery import Celery

backend = 'redis://127.0.0.1:6379/0'
broker = 'redis://127.0.0.1:6379/1'

app = Celery('tasks', backend=backend, broker=broker)


@app.task
def add(x, y):
    sleep(10)
    return x + y