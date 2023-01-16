import random
import json
import base64
import uuid
import os





def get_json(file_name):
    file = open(file_name, "r")
    content = file.read()
    file.close()
    json_content = json.loads(content)
    return json_content


def put_json(file_name, json_content):
    file = open(file_name, "w")
    file.write(json.dumps(json_content))
    file.close()
    return True


def conf(info):
    file = open("config.conf", "r")
    content = file.read()
    file.close()
    got_info = content.split("|")
    if info == "ip":
        return got_info[0]
    elif info == "docker":
        return got_info[1]
    else:
        return False



def make_link(uuuid, port, name):
    ip = conf("ip")
    link = '{"add":"'+ ip +'","aid":"0","host":"","id":"'+ uuuid +'","net":"ws","path":"/graphql","port":"'+ str(port) +'","ps":"'+ name +'","scy":"auto","sni":"","tls":"","type":"","v":"2"}'
    encoded_link = base64.b64encode(str.encode(link))
    return "vmess://" + encoded_link.decode("utf-8")



def add_user(name, port, data_limit, time_limit, admin_id):
    content = get_json("config.json")
    uuuid = str(uuid.uuid4())[:-1] + "a"
    email = uuuid + "@gmail.com"
    new_user = {"user" : {"name" : name, "admin" : admin_id, "data-limit" : data_limit, "time-limit" : time_limit}, "port": int(port), "protocol": "vmess", "allocate": {"strategy": "always"}, "settings": {"clients": [{"id": uuuid, "level": 1, "alterId": 0, "email": email}], "disableInsecureEncryption": True}, "streamSettings": {"network": "ws", "wsSettings": {"connectionReuse": True, "path": "/graphql"}, "security": "none", "tcpSettings": {"header": {"type": "http", "response": {"version": "1.1", "status": "200", "reason": "OK", "headers": {"Content-Type": ["application/octet-stream", "application/x-msdownload", "text/html", "application/x-shockwave-flash"], "Transfer-Encoding": ["chunked"], "Connection": ["keep-alive"], "Pragma": "no-cache"}}}}}}
    content["inbounds"].append(new_user)
    put_json("config.json", content)
    os.system("docker restart " + conf("docker"))
    os.system("iptables -A INPUT -p tcp --dport " + str(port))
    os.system("iptables -A OUTPUT -p tcp --sport " + str(port))
    os.system("sudo /sbin/iptables-save")
    print(make_link(uuuid, port, name))


def delete_user(port):
    content = get_json("config.json")
    num = 0
    for i in content["inbounds"]:
        if i["port"] == port:
            content["inbounds"].pop(num)
            break
        num = num + 1
    put_json("config.json", content)
    os.system("docker restart " + conf("docker"))
    os.system("iptables -D INPUT -p tcp --dport " + str(port))
    os.system("iptables -D OUTPUT -p tcp --sport " + str(port))
    os.system("sudo /sbin/iptables-save")


def get_user_info(port):
    content = get_json("config.json")
    info = {}
    for i in content["inbounds"]:
        if i["port"] == port:
            info = {"name": i["user"]["name"], "admin": i["user"]["admin"], "data-limit": i["user"]["data-limit"], "time-limit": i["user"]["time-limit"], "uuid": i["settings"]["clients"][0]["id"], "port": i["port"]}
            return info


#print(make_link(get_user_info(80)["uuid"], get_user_info(80)["port"], get_user_info(80)["name"]))


def get_users(admin_id):
    content = get_json("config.json")
    users = []
    for i in content["inbounds"]:
        if i["user"]["admin"] == admin_id:
            users.append(get_user_info(i["port"]))
            break
    print(users)

#get_users(1920631160)












