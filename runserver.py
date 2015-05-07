# -*- coding: utf-8 -*-
__author__ = 'florije'

"""
celery command:
celery --app=runserver.celery worker --loglevel=info
"""

from flask import Flask, jsonify, request
from celery import Celery
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

handler = TimedRotatingFileHandler(filename='{0}'.format('logs.log'),
                                   when='D', interval=1, backupCount=5)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


def make_celery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task()
def add_log(msg):
    app.logger.warning(msg=msg)
    return msg


@app.route('/')
def hello_world():
    add_log.apply_async((request.host, ))
    return jsonify(result='success'), 200


if __name__ == '__main__':
    app.run(debug=True)