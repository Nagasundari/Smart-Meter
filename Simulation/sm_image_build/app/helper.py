import os
from flask import Flask, request, jsonify
from flask_cors import cross_origin


fport = int(os.environ["fport"])
meter_id = os.environ["meter_id"]

app = Flask(__name__)

@app.route('/get_current')
@cross_origin()
def get_current():
    current = ""
    with open("data.txt", "r") as f:
        current = f.read()
    return current, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=fport + 1000, debug = False)
