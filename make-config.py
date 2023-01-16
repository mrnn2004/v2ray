import subprocess
import os
import time


os.system("docker exec -it e2a519f4b60a truncate -s 0 access.log")
print("---------------------------------------------------------")
time.sleep(5)

subprocess1 = subprocess.Popen("docker exec -it e2a519f4b60a cat access.log", shell=True, stdout=subprocess.PIPE)
subprocess_return = subprocess1.stdout.read()
log_array = subprocess_return.decode("utf-8").splitlines()
for i in log_array:
    print(i.split())
print("---------------------------------------------------------")

