#!/usr/bin/env python3

import flask
import json
import shutil
import logging
import logging.handlers
import socket


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


@app.route('/api/send/udp/', methods=['GET'])
def send_udp():
    handler = logging.handlers.SysLogHandler(address = ('0.0.0.0',514),  socktype=socket.SOCK_STREAM)
    my_logger.addHandler(handler)
    List1 = ['test1','test2','test3']
    for row in List1:
        my_logger.info("" +row+'\n')
        my_logger.handlers[0].flush()
    return resp(200, {"result": "ok"})


@app.route('/api/send/tcp/', methods=['GET'])
def send_tcp():
    handler = logging.handlers.SysLogHandler(address = ('localhost',514),  socktype=socket.SOCK_STREAM)
    my_logger.addHandler(handler)
    List1 = ['test1','test2','test3']
    for row in List1:
        my_logger.info("" +row+'\n')
        my_logger.handlers[0].flush()
    return resp(200, {"result": "ok"})


if __name__ == '__main__':
    app.debug = True 
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=8085)