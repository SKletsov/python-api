#!/usr/bin/env python3

import flask
import json
import os
import shutil
import uuid
import time
import logging
import logging.handlers
import socket
import subprocess



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


def send_udp():
    handler = logging.handlers.SysLogHandler(address = ('0.0.0.0',514),  socktype=socket.SOCK_STREAM)
    my_logger.addHandler(handler)
    timeRecord = getUnixTime()
    my_logger.info("" +timeRecord+'\n')
    my_logger.handlers[0].flush()
    send = getFileData(timeRecord)
    return send


def send_tcp():
    handler = logging.handlers.SysLogHandler(address = ('0.0.0.0',514),  socktype=socket.SOCK_STREAM)
    my_logger.addHandler(handler)
    timeRecord = getUnixTime()
    my_logger.info("" +timeRecord+'\n')
    my_logger.handlers[0].flush()
    send = getFileData(timeRecord)
    return send


def getUnixTime():
    row = str(round(time.time() * 1000000000))
    return row 

def getFileData(unix):
    time.sleep(10)
    cmd = "docker exec  -it  rsyslog grep -R '"+unix+"'  /var/log/remote/* | wc -l"
    returned_output = subprocess.check_output(cmd)
    print('Current date is:', returned_output.decode("utf-8"))
    print('cmd',cmd)
    if int(returned_output.decode("utf-8")) >= 1 :
        return True
    else:
       return False


@app.route('/api/checker/', methods=['GET'])
def get_results():
    total, used, free = shutil.disk_usage("/")
    if used / total * 100 >= 90:
             return resp(503, {"error": "memory is "+free+""})
    else:
       print ("analize socket")
       dataTCP = send_tcp()
       dataUDP = send_udp()
       if dataTCP == False or dataUDP == False :
           return resp(500, {"result": "error"})
       else:
           return resp(200, {"result": "error"})
 

if __name__ == '__main__':
    app.debug = True 
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=8080)