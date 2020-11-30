from flask import Flask, request, jsonify
from flask_cors import cross_origin
from collections import deque
from datetime import datetime

app = Flask(__name__)

dataq = deque()
dataq.extend([(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)
              ])

current = 0.0
usage = 0.0


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
    global current
    global usage
    current = request.form['current']
    usage = request.form['usage']
    now = datetime.now()
    print("Current: ", request.form['current'],
          " Usage: ", request.form['usage'])
    dataq.popleft()
    dataq.append((now.strftime("%d/%m, %H:%M:%S"), request.form['current']))
    return "", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
