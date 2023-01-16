import subprocess
from types import CoroutineType
import requests



'''while True:

    subprocess1 = subprocess.Popen("tcpdump port 28501 and not src 45.195.200.248 -q -c 1", shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess1.stdout.read()

    text = subprocess_return.decode("utf-8")
    text1 = text.split(" ")
    text2 = text1[2].split(".")
    text3 = str(text2[0]) + "." + str(text2[1]) + "." + str(text2[2]) + "." + str(text2[3])

    url = "http://ip-api.com/json/" + text3
    city = requests.get(url).json()

    print("---------------------------------------------------------------------------------> ip : " + text3 + " - city : " + city["city"])
'''

all_ips = []
while True:
    subprocess1 = subprocess.Popen("timeout 60 tcpdump port 80 and not src 156.255.1.217 -q", shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess1.stdout.read()

    line_list = subprocess_return.decode("utf-8").splitlines()
    for i in line_list:
        if i:
            line = i.split()
            ip = line[2].split(".")
            if len(ip) == 5:
                ip1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(ip[3])
                all_ips.append(ip1)



    print("----------------------------------------------------------------------------------------")
    print(str(len(all_ips)))
    all_ips = list(set(all_ips))
    print(str(len(all_ips)))
    print(all_ips)
    print("----------------------------------------------------------------------------------------")
    all_ips = []

