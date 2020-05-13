#!/usr/bin/env python3

import flask
import json

app = flask.Flask(__name__)

def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )



@app.route('/api/data', methods=['GET'])
def get_results():
    return resp(200, {"result": "test"})


if __name__ == '__main__':
    app.debug = True 
    app.run(host='0.0.0.0', port=8085)