import subprocess
import time
from datetime import datetime



def users():
    subprocess1 = subprocess.Popen("ss -tn src :80", shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess1.stdout.read()
    line_list = subprocess_return.decode("utf-8").splitlines()

    all_ips = []
    for i in line_list:
        text = i.split()[-1].replace("[::ffff:", "")
        text1 = text.split("]:")
        if text1[0] != "Process":
            all_ips.append(text1[0])
    all_ips = list(set(all_ips))
    return all_ips

                                                           
file = open("connected-users.log", "a")       
while True:
    text = str(datetime.now()) + "|" + str(len(users())) + "\n"
    #file.write(text)
    #print(datetime.now())
    print(str(len(users())))
    time.sleep(5)

file.close()
