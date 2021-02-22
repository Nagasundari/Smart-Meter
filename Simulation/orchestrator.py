import docker
import sys
from flask import Flask, jsonify
from flask_cors import cross_origin
import threading
import requests
import ast

# Define all variables
start_port = 5002

meters = dict()

meter_port_map = dict()

no_of_meters = int(sys.argv[1])

client = docker.from_env()

rasp_url = "http://localhost:5000"

temp_nws = []
for i in client.networks.list():
    temp_nws.append(i.name)

if 'rasp_network' not in temp_nws:
    client.networks.create("rasp_network", driver="bridge")


def start_containers():
    for i in range(3, no_of_meters + 3):
        meter_id = "sm" + str(i)
        port = start_port + i
        container = None
        try:
            container = client.containers.run(name=meter_id, image="sm_image",
                                              environment={
                                                  "meter_id": meter_id, "fport": port},
                                              detach=True,
                                              ports={str(port)+'/tcp': port
                                                     }, network="rasp_network"
                                              )
        except:
            pass
        meters[meter_id] = {
            "port": port,
            "handle": container
        }
        meter_port_map[meter_id] = port
    print(meters)


threading.Thread(target=start_containers, args=()).start()

app = Flask(__name__)


@app.route('/change_state/<sm_id>/<dev_id>/<status>')
@cross_origin()
def change_state(sm_id, dev_id, status):
    global meter_port_map
    r = requests.get("http://localhost" + ":" + str(meter_port_map[sm_id]) + "/change_state/" + dev_id + "/" + status)
    return "DONE", 200

@app.route('/get_meters_name_port')
@cross_origin()
def get_meters_name_port():
    global meter_port_map
    return jsonify(meter_port_map), 200

@app.route('/get_devices/<sm_id>')
@cross_origin()
def get_devices(sm_id):
    global meter_port_map
    r = requests.get("http://localhost" + ":" + str(meter_port_map[sm_id]) + "/get_devices")
    data = ast.literal_eval(r.text)
    return jsonify(data), 200

@app.route('/get_rasp_current')
@cross_origin()
def get_rasp_current():
    print("sent", rasp_url + "/get_rasp_current")
    return requests.get(rasp_url + "/get_rasp_current").text, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
