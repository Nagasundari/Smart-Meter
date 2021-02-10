import time
import requests

curr_map = {'b': 1,
            'f': 2,
            't': 3
            }

current = 0
usage = 0


meter_id = "sm01"
server_url = "https://hci-flask.run-ap-south1.goorm.io"

dev = ['b', 'b', 'f', 'f', 't']

runt = [0, 1000]


def tCheck():
    if(time.time() * 1000 > runt[0] + runt[1]):
        return True
    return False


def tRun():
    runt[0] = time.time() * 1000


current = 0
usage = 0


def func1():
    global usage
    temp = 0
    for i in dev:
        temp += curr_map[i]
    current = temp
    usage += ((230.0 * current) / 3600000.0)
    print(usage)
    requests.post(server_url, data={
                  "current": current, "usage": usage, "meter_id": meter_id})


def check():
    pass


runt[0] = time.time()
while True:
    if (tCheck()):
        tRun()
        func1()
        check()
