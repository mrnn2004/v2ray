import os
import base64
import uuid
import json
import time
import calendar




def port_to_uuid(port):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    if ("|" + str(port) + "|") in i:
      uid = i.split("|")[0]
      return uid
      break

def port_to_id(port):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    if ("|" + str(port) + "|") in i:
      id = i.split("|")[4]
      return id
      break

def get_max_data(port):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    if ("|" + str(port) + "|") in i:
      max_data = i.split("|")[3]
      return max_data
      break

def get_date(port):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    if ("|" + str(port) + "|") in i:
      date = i.split("|")[6]
      return date
      break

def link_to_port(link):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    if ("|" + link + "|") in i:
      port = i.split("|")[1]
      return port
      break

def port_to_link(port):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    if ("|" + str(port) + "|") in i:
      link = i.split("|")[5]
      return link
      break

def port_to_full_data(port):
  file = open("users.conf", "r")
  content = file.read()
  file.close()
  all_lines = content.splitlines()
  for i in all_lines:
    user_info = i.split("|")
    if str(port) == user_info[1]:
      return i
      break



#def set_new_data(port, data):






def add_user(ip, port, id, max_data, date, name="v2ray"):
    file = open("config.json", "r")
    file_content = json.loads(file.read())
    file.close()
    uuuid = str(uuid.uuid4())[:-1] + "a"
    email = uuuid + "@gmail.com"
    new_user = {"port": int(port), "protocol": "vmess", "allocate": {"strategy": "always"}, "settings": {"clients": [{"id": uuuid, "level": 1, "alterId": 0, "email": email}], "disableInsecureEncryption": True}, "streamSettings": {"network": "ws", "wsSettings": {"connectionReuse": True, "path": "/graphql"}, "security": "none", "tcpSettings": {"header": {"type": "http", "response": {"version": "1.1", "status": "200", "reason": "OK", "headers": {"Content-Type": ["application/octet-stream", "application/x-msdownload", "text/html", "application/x-shockwave-flash"], "Transfer-Encoding": ["chunked"], "Connection": ["keep-alive"], "Pragma": "no-cache"}}}}}}
    file_content["inbounds"].append(new_user)
    file = open("config.json", "w")
    file.write(json.dumps(file_content))
    file.close()


    os.system("docker restart e2a519f4b60a")
    link = '{"add":"'+ ip +'","aid":"0","host":"","id":"'+ uuuid +'","net":"ws","path":"/graphql","port":"'+ str(port) +'","ps":"'+ name +'","scy":"auto","sni":"","tls":"","type":"","v":"2"}'
    encoded_link = base64.b64encode(str.encode(link))
    finall_link = "vmess://" + encoded_link.decode("utf-8")
    print(finall_link)
    os.system("iptables -A INPUT -p tcp --dport " + str(port))
    os.system("iptables -A OUTPUT -p tcp --sport " + str(port))

    file = open("users.conf", "a")
    file.write(uuuid + "|" + str(port) + "|" + name + "|" + str(int(max_data)) + "|" + str(id) + "|" + finall_link + "|" + str(date) + "\n")
    file.close()
    os.system("sudo /sbin/iptables-save")



#current_GMT = time.gmtime()
#time_stamp = calendar.timegm(current_GMT)
#add_user("45.195.200.248", 7346, 2233862700, 10, time_stamp+3600, "10mb data use")
#add_user("45.195.200.248", 2269, 1920631160, 5, time_stamp+3600, "5mb data use")
#add_user("45.195.200.248", 3453, 1920631160, 100, time_stamp+3600, "100mb data use")
#add_user("45.195.200.248", 9980, 1920631160, 20, time_stamp+3600, "20mb data use")




def delete_user(ip, port):
  file = open("config.json", "r")
  content = file.read()
  file.close()
  full_array = json.loads(content)
  num = 0
  for i in full_array["inbounds"]:
    uid = i["settings"]["clients"][0]["id"]
    if port == i["port"]:
      del full_array["inbounds"][num]
      file = open("config.json", "w")
      file.write(json.dumps(full_array))
      file.close()

      os.system("docker restart e2a519f4b60a")
      port = str(i["port"])
      name = i["settings"]["clients"][0]["email"].split("@")[1]
      os.system("iptables -D INPUT -p tcp --dport " + port)
      os.system("iptables -D OUTPUT -p tcp --sport " + port)
      file = open("users.conf", "r")
      content = file.read()
      file.close()
      content1 = content.replace(port_to_full_data(port) + "\n", "")
      file = open("users.conf", "w")
      file.write(content1)
      file.close()
      os.system("sudo /sbin/iptables-save")
      break
    num = num + 1



#delete_user("45.195.200.248", 32693)
#delete_user("45.195.200.248", 2269)
#delete_user("45.195.200.248", 3453)
#delete_user("45.195.200.248", 9980)



def disable_enable(port, status):
  file = open("config.json", "r")
  file_content = file.read()
  file.close()
  file = open("users.conf", "r")
  users_file = file.read()
  file.close()
  uuuid = port_to_uuid(port)
  if uuuid in file_content:
    if status == "disable":
      eddited_file = file_content.replace(uuuid, (uuuid[:-1]+"e"))
      file = open("config.json", "w")
      file.write(eddited_file)
      file.close()
      eddited_file = users_file.replace(uuuid, (uuuid[:-1]+"e"))
      file = open("users.conf", "w")
      file.write(eddited_file)
      file.close()

      os.system("docker restart e2a519f4b60a")
      print("user with uuid " + uuuid + " now is disabled ...")
    elif status == "enable":
      eddited_file = file_content.replace(uuuid, (uuuid[:-1]+"a"))
      file = open("config.json", "w")
      file.write(eddited_file)
      file.close()
      eddited_file = users_file.replace(uuuid, (uuuid[:-1]+"a"))
      file = open("users.conf", "w")
      file.write(eddited_file)
      file.close()

      os.system("docker restart e2a519f4b60a")
      print("user with uuid " + uuuid + " now is enabled ...")
  else:
    print("user not fpund")

#disable_enable(2269, "enable")


