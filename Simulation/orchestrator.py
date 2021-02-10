import docker
import sys

# Define all variables
start_port = 5002


meters = dict()

meter_port_map = dict()

no_of_meters = int(sys.argv[1])

client = docker.from_env()

for i in range(3, no_of_meters + 3):
    meter_id = "sm" + str(i)
    port = start_port + i
    container = client.containers.run(name=meter_id, image="sm_image",
                                      environment={
                                          "meter_id": meter_id, "fport": port},
                                      detach=True,
                                      ports={str(port)+'/tcp': port
                                            })
    meters[meter_id] = {
        "port": port,
        "handle": container
    }

print(meters)