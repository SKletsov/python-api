#!/usr/bin/env python3

import os
import shutil
import uuid
import time
import logging
import logging.handlers
import socket
import subprocess


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

def get_results():
    total, used, free = shutil.disk_usage("/")
    if used / total * 100 >= 90:
             writeFile('{"error": "memory is closed "}')
    else:
       print ("analize socket")
       dataTCP = send_tcp()
       dataUDP = send_udp()
       if dataTCP == False or dataUDP == False :
           writeFile('{"error": "tcp or udp failed "}')
       else:
           writeFile('{ok": "ok "}')
 

def writeFile(data):
    print("Data",data)
    f = open('./python.log', 'w')
    f.write(data)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

if __name__ == '__main__':
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)
    get_results()