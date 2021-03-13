from flask import Flask, request, jsonify
from flask_cors import cross_origin
from collections import deque
from datetime import datetime
import pytz
import logging
import ast
import threading
import requests
import hashlib

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

meters = dict()
usage = 0
glob_current = 0

IST = pytz.timezone('Asia/Kolkata')
# file = open("data.csv", "a+")
# file.write("Date, Time, Current, Usage" + "\r\n")

main_server_url = "https://capstonens05.run-ap-south1.goorm.io"


def create_meter_data_dict(meter_id):
    global meters
    meters[meter_id] = {
        "meter_id": meter_id,
        "dataq": deque()
    }


def send_data(meter_id):
    data = dict()
    data['meter_id'] = meters[meter_id]['meter_id']
    data['dataq'] = list(meters[meter_id]['dataq'])
    r = requests.post(url=main_server_url, json=data)
    # print(r)


def append_data(meter_id, current, usage, time):
    meters[meter_id]['dataq'].append([time, current, usage])
    #print("len: ", len(meters[meter_id]['dataq']))
    if (len(meters[meter_id]['dataq']) > 3):
        try:
            send_data(meter_id)
        except:
            pass
        meters[meter_id]['dataq'].clear()
        # print(meters[meter_id]['dataq'])


@app.route('/')
def send():
    return "hello", 200


def collectData():
    global glob_current
    global usage
    threading.Timer(1, collectData).start()
    r = requests.get('http://192.168.1.110:5001/get_meters_name_port')
    meters_port_map = ast.literal_eval(r.text)
    print(meters_port_map)
    curVal = 0
    try:
        for meter_id in meters_port_map:
            print("http://" + meter_id + ":" +
                  str(meters_port_map[meter_id]) + "/get_current")
            curVal += int(ast.literal_eval(requests.get("http://" + meter_id +
                                                        ":" + str(meters_port_map[meter_id]) + "/get_current").text))
            print(curVal)
        glob_current = curVal
        usage += ((230.0*curVal)*curVal)/3600000.0
    except:
        pass


@app.route('/get_rasp_current')
def get_rasp_current():
    return str(glob_current), 200


@app.route('/', methods=['POST'])
def recv():
    global meters
    current = request.form['current']
    usage = request.form['usage']
    meter_id = request.form['meter_id']
    hash = request.form['hash']
    dk = hashlib.pbkdf2_hmac('sha256', bytes("current=" + str(current) + ";" + "usage=" + str(usage), 'utf-8'), bytes(meter_id, 'utf-8'), 37)
    print("current:", current)
    print("usage:", usage)
    print("meter_id:", meter_id)
    print("hash", hash)
    print("dk.hex()", dk.hex())
    if (str(dk.hex()) != hash):
        return "Not Acceptable", 406

    if (meter_id not in meters):
        create_meter_data_dict(meter_id)
    now = datetime.now(IST)
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    # print("--------------------------", time,"---------------------------")
    # print("meter_id:", meter_id, "Current: ", request.form['current'], " Usage: ", request.form['usage'])
    # print("------------------------------------------------------------------")
    append_data(meter_id, current, usage, time)
    # file.write(now.strftime("%d/%m/%y, %I:%M:%S %p") + ", " + str(request.form['current']) + ", " + str(request.form['usage']) + "\r\n")
    return "", 200


if __name__ == '__main__':
    collectData()
    app.run(host='0.0.0.0', port=5000, debug=False)
