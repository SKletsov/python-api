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



@app.route('/api/checker/', methods=['GET'])
def get_results():
    ###read from file 
    lines = open("./python.log").read()
    os.remove("./python.log")
    print(lines)
    if lines.find("ok") == -1:
     return resp(500, {"error": ""+str(lines)+""})  
    else:
     print("Found 'is' in the string.")
     return resp(200, {"result": "ok"})   
    
    

if __name__ == '__main__':
    app.debug = True 
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=8085)