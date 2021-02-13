from flask import Flask, request, jsonify
from flask_cors import cross_origin
from collections import deque
from datetime import datetime
import pytz
import logging
import requests

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

meters = dict()

IST = pytz.timezone('Asia/Kolkata') 
file = open("data.csv", "a+")
file.write("Date, Time, Current, Usage" + "\r\n")

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
    r = requests.post(url = main_server_url, json = data)
    print(r)
    

def append_data(meter_id, current, usage, time):
    meters[meter_id]['dataq'].append([time, current, usage])
    print("len: ", len(meters[meter_id]['dataq']))
    if (len(meters[meter_id]['dataq']) > 3):
        try:
            send_data(meter_id)
        except:
            pass
        meters[meter_id]['dataq'].clear()
        print(meters[meter_id]['dataq'])
    

@app.route('/')
def send():
    return "hello", 200

@app.route('/dataforplot')
@cross_origin()
def dataforplot():
    global current
    global usage
    dt = list(dataq)
    data = {
        'x': [a[0] for a in dt],
        'y': [a[1] for a in dt],
        'usage': usage,
        'current': current
    }
    return jsonify(data), 200

@app.route('/', methods=['POST'])
def recv():
    global meters
    current = request.form['current']
    usage = request.form['usage']
    meter_id = request.form['meter_id']
    if (meter_id not in meters):
        create_meter_data_dict(meter_id)
    now = datetime.now(IST)
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("--------------------------", time,"---------------------------")
    print("meter_id:", meter_id, "Current: ", request.form['current'], " Usage: ", request.form['usage'])
    # print("------------------------------------------------------------------")
    append_data(meter_id, current, usage, time)
    file.write(now.strftime("%d/%m/%y, %I:%M:%S %p") + ", " + str(request.form['current']) + ", " + str(request.form['usage']) + "\r\n")
    return "", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = False)

