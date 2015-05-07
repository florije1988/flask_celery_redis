# -*- coding: utf-8 -*-
__author__ = 'florije'

import os
from flask import Flask, jsonify
from celery import Celery
from flask_mail import Mail, Message

"""
celery command:
celery --app=flask_demo.celery worker --loglevel=info
"""

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '296701047@qq.com'  # os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'password'  # os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = '296701047@qq.com'

mail = Mail(app)


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        mail.send(msg)
    return 'success'


@app.route('/', methods=['GET', 'POST'])
def index():
    # send the email
    msg = Message('Hello from Flask', recipients=["945744127@qq.com"])
    msg.body = 'This is a test email sent from a background Celery task.'

    # send_async_email.delay(msg)
    # send_async_email.apply_async(args=[msg], countdown=60)
    send_async_email.apply_async(args=[msg])

    return jsonify(result='success'), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')