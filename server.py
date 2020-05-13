#!/usr/bin/env python3

import flask
import json
import shutil

app = flask.Flask(__name__)

def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )

@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.route('/api/memory', methods=['GET'])
def get_results():
    total, used, free = shutil.disk_usage("/")
    if used / total * 100 >= 90:
             return resp(500, {"result": free})
    return resp(200, {"result": free})


if __name__ == '__main__':
    app.debug = True 
    app.run(host='0.0.0.0', port=8085)