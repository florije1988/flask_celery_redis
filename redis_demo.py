# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, jsonify
from flask.ext.redis import FlaskRedis
import simplejson


app = Flask(__name__)
redis_store = FlaskRedis(app)
app.config['REDIS_URL'] = 'redis://localhost:6379/0'

@app.route('/', methods=['GET', 'POST'])
def index():
    user_info = {'name': 'florije', 'age': 20}
    redis_store.set('user_info', simplejson.dumps(user_info))
    raw_user_info = redis_store.get('user_info')
    user_info_obj = simplejson.loads(raw_user_info)
    return jsonify(name=user_info_obj['name'], age=user_info_obj['age'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
