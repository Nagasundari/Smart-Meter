import requests
import time
import random
currents = [10, 11, 12 ,13]
usage = 0
while(True):
	curVal = random.choice(currents)
	usage += ((230.0*curVal)*curVal)/3600000.0
	requests.post("http://localhost:5000", data = {"meter_id": "sm3", "current": curVal, "usage": usage})
	#time.sleep(1000)
