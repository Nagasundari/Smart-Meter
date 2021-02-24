from flask import Flask, request, jsonify
import random
import threading
import requests
import os
from flask_cors import cross_origin
import datetime

fport = int(os.environ["fport"])
meter_id = os.environ["meter_id"]

app = Flask(__name__)

usage = 0  # keeps track of total usage
status = {}  # gets the status of bulb or fan
current = {}  # keeps track current usage of perticular device

glob_current = 0

B = 2  # number of bulb
F = 2  # number of fan

serverUrl = "http://rasp_server:5000"  # server url

pos = {'B': [], 'F': []}  # keeps track of bulb or fan number

# helper function
# ......................................................................................................................................


def initAppliance():  # intialises appliance
    current['B'] = 2
    current['F'] = 2

    for i in range(1, B+1):
        status['B'+str(i)] = 1
        pos['B'].append(i)

    for i in range(1, F+1):
        status['F'+str(i)] = 1
        pos['F'].append(i)

def getNewPos(lst):  # checks for new bulb or fan number starting from 1
    cur = 1
    while cur in lst:
        cur += 1
    return cur

# ..........................................................
# flask function
# gets the total device status
# no body required
@app.route("/getReadings")
@cross_origin()
def getReadings():
    return jsonify(status)


# updates the given device
# format : {'B1':1, B2: 0, ..}
@app.route("/updateReadings")
@cross_origin()
def updateReadings():
    data = request.get_json()

    for device in data:
        status[device] = data[device]

    return "Updated Successfully", 200

# adds the device to current infrastructure
# format : {B:2, F:3}


@app.route("/addDevice")
@cross_origin()
def addDevice():
    data = request.get_json()
    for device in data:
        if device == 'B':
            num = data[device]
            for i in range(num):
                val = getNewPos(pos['F'])
                status['F'+str(val)] = 1
                pos['F'].append(val)

        elif device == 'F':
            num = data[device]
            for i in range(num):
                val = getNewPos(pos['F'])
                status['F'+str(val)] = 1
                pos['F'].append(val)
    return "Added Successfully", 200

# ...............................................................
# sends the reading to server at the interval of every 1 second

@app.route("/change_state/<dev_id>/<stat>")
@cross_origin()
def change_state(dev_id, stat):
    dev_id = dev_id.upper()
    if (stat == 'on'):
        status[dev_id] = 1
    else:
        status[dev_id] = 0
    return "DONE", 200

@app.route("/get_devices")
@cross_origin()
def get_devices():
    global status
    return jsonify(status), 200

@app.route("/get_current")
@cross_origin()
def get_current():
    global glob_current
    return str(glob_current), 200


def sendUsage():
    threading.Timer(1, sendUsage).start()
    curVal = 0
    global usage
    global glob_current
    for key in status:
        if status[key]:
            curVal += current[key[0]]
    
    glob_current = curVal
    usage += ((230.0*curVal)*curVal)/3600000.0
    with open("data.txt", "w") as f:
        f.write(str(glob_current))
    #print(status)
    #print(meter_id, curVal, usage)
    #print(datetime.datetime.now())
    requests.post(serverUrl, data={
                  "meter_id": meter_id, "current": curVal, "usage": usage})  # change this


if __name__ == "__main__":
    initAppliance()
    sendUsage()
    app.run(host='0.0.0.0', port=fport, debug = False)
