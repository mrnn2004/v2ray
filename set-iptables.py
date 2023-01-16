import os


file = open("users.conf", "r")
content = file.read()
file.close()


content_list = content.splitlines()
for i in content_list:
    port = i.split("|")[1]
    os.system("iptables -A INPUT -p tcp --dport " + str(port))
    os.system("iptables -A OUTPUT -p tcp --sport " + str(port))


os.system("sudo iptables-save > /root/working.iptables.rules")
