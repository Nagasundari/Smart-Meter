from flask import Flask, request, jsonify
import random
import threading
import requests
import os

fport = int(os.environ["fport"])
meter_id = os.environ["meter_id"]

app = Flask(__name__)

usage = 0  # keeps track of total usage
status = {}  # gets the status of bulb or fan
current = {}  # keeps track current usage of perticular device

B = random.randint(1, 4)  # number of bulb
F = random.randint(1, 3)  # number of fan
serverUrl = "http://192.168.1.111:5000"  # server url

pos = {'B': [], 'F': []}  # keeps track of bulb or fan number

# helper function
# ......................................................................................................................................


def initAppliance():  # intialises appliance
    current['B'] = 1
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
def getReadings():
    return jsonify(status)


# updates the given device
# format : {'B1':1, B2: 0, ..}
@app.route("/updateReadings")
def updateReadings():
    data = request.get_json()

    for device in data:
        status[device] = data[device]

    return "Updated Successfully", 200

# adds the device to current infrastructure
# format : {B:2, F:3}

@app.route("/addDevice")
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


def sendUsage():
    threading.Timer(1, sendUsage).start()
    curVal = 0
    global usage
    for key in status:
        if status[key]:
            curVal += current[key[0]]

    usage += ((230.0*curVal)*curVal)/3600000.0

    print(usage, curVal)  # name = set in env
    requests.post(serverUrl, data={"meter_id": meter_id, "current": curVal, "usage": usage})  # change this


if __name__ == "__main__":
    initAppliance()
    sendUsage()
    app.run(host='0.0.0.0', port=fport)