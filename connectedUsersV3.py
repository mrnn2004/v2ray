import os
import subprocess
import time
import calendar
from threading import Thread
from functions import *

all_info = '{'

def connected(port):
    global all_info
    all_ips = []
    current_GMT = time.gmtime()
    current_time = calendar.timegm(current_GMT)
    target_time = current_time + 20
    while current_time <= target_time:

        command = 'netstat -anp | grep "156.255.1.217:'+ str(port) +' " | grep ESTABLISHED | grep -v "  0      0 "'
        subprocess1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        subprocess_return = subprocess1.stdout.read()
        line_list = subprocess_return.decode("utf-8").splitlines()
        for i in line_list:
            ip = i.split()[4].split(":")[0]
            if not ip in all_ips:
                all_ips.append(ip)
        current_GMT = time.gmtime()
        current_time = calendar.timegm(current_GMT)
        time.sleep(0.050)
    print(all_ips)
    info = '"'+str(port)+'"' + " : " + str(len(all_ips)) + ", "
    all_info = all_info + info
    #all_info.append(info)


connected(14620)





'''all_ports = {100:20, 200:10}
put_json("connected-users.json", all_ports)'''














