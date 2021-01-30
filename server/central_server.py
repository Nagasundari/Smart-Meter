from flask import Flask, request, jsonify
from flask_cors import cross_origin
from collections import deque
from datetime import datetime
from pprint import pprint
import pytz
import logging
import sqlite3

def sql_insert(meter_id, entities):
    con = sqlite3.connect('smart_meter.db')
    cursorObj = con.cursor()
    cursorObj.execute('''CREATE TABLE IF NOT EXISTS ''' + meter_id + ''' (time_date TEXT, current REAL, usage REAL);''')
    cursorObj.execute('INSERT INTO ' + meter_id + '(time_date, current, usage) VALUES(?, ?, ?);', entities)
    con.commit()
    con.close()

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/')
def send():
    return "hello", 200

@app.route('/dataforplot')
@cross_origin()
def dataforplot():
    global current
    global usage
    dt = list()
    data = {
        'x': [a[0] for a in dt],
        'y': [a[1] for a in dt],
        'usage': usage,
        'current': current
    }
    return jsonify(data), 200


@app.route('/', methods=['POST'])
def recv():
    pprint(request.json)
    meter_id = request.json['meter_id']
    dataq = request.json['dataq']
    for i in dataq:
        sql_insert(meter_id, tuple(i))
    return {},200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)