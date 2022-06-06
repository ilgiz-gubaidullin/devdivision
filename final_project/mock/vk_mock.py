#!/usr/bin/env python3.10

import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    if username == 'user_no_vk_id':
        response = jsonify({})
        response.status_code = 404
        response.headers["Content-Type"] = "application/json"
        return response
    elif username:
        response = jsonify({'vk_id': 12345678})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == '__main__':
    host = os.environ.get('VK_API_HOSTNAME', '0.0.0.0')
    port = os.environ.get('VK_API_PORT', '8005')

    app.run(host, port)
    app.run()
