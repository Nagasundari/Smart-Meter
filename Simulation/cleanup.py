import docker
import threading

client = docker.from_env()

to_stop = []
for i in client.containers.list(all = True):
    if "sm" in i.name:
        to_stop.append(i)

def stop_container(handle):
    handle.stop()
    handle.remove()

threads = []
for i in to_stop:
    threads.append(threading.Thread(target=stop_container, args=(i,)))

for i in threads:
    i.start()