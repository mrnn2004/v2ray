# Importing the relevant libraries
import websockets
import asyncio
from adminsManage import *
from dataUsage import *
from usersManage import *
import time
from threading import Thread
import calendar
import random
from functions import get_json


PORT = 3000
print("Server listening on Port " + str(PORT))



all_clients = []
async def echo(websocket):
    all_clients.append(websocket)
    print('A client just connected')
    try:
        async for message in websocket:
            print(message)
            if message.startswith("|+34>-)-*|"):
                user_pass = message.replace("|+34>-)-*|", "").split("|<-->|")
                is_admin = check_admin(str(user_pass[0]), str(user_pass[1]))
                if is_admin != False:
                    text2 = ""
                    found_users = users_list(is_admin)
                    all_connected = 0
                    for i in found_users:
                        user_info = i.split("|")
                        used_data = data_usage(user_info[1]).split(":")
                        used_data = (int(used_data[0]) + int(used_data[1]))
                        max_data = user_info[3]
                        current_GMT = time.gmtime()
                        current_time = calendar.timegm(current_GMT)
                        ex_time = int(get_date(user_info[1]))
                        time_left = (ex_time - current_time)/86400
                        all_users_connected = get_json("connected-users.json")
                        if str(user_info[1]) in all_users_connected:
                            connected_users_to_this_port = str(all_users_connected[str(user_info[1])])
                        else:
                            connected_users_to_this_port = "0"
                        all_connected = all_connected + int(connected_users_to_this_port)

                        if float(used_data) < float(max_data) and time_left > 0:
                            if user_info[0][-1] != "a":
                                disable_enable(user_info[1], "enable")

                            text2 = text2 + '''<div class="name enable">'''+ str(user_info[2]) +'''<div style="background-color: #ffffff80;float: left;padding: 0 20px;">'''+connected_users_to_this_port+'''</div></div><div class="status enable" style="font-family: tahoma;">enable</div><div class="data-usage enable"><div style="float: left;border-style: none;padding: 0px;" onclick="new_data_limit()">edit</div>'''+ str(int(used_data)/1000) + '''GB | ''' + str(float(max_data)/1000) +'''GB</div><div class="date enable">'''+ str(round(time_left, 1)) +''' Days</div><div class="vmess-link enable" data-vmess="'''+ user_info[5] +'''" onclick="copyToClipboard(this.getAttribute('data-vmess'));"><div style="text-align: center; width: 100%;">click to copy</div>'''+ user_info[5] +'''</div><div class="qrcode enable" data-vmess="'''+ user_info[5] +'''" onclick="makeCode(this.getAttribute('data-vmess'));"><div style="text-align: center; width: 100%;">Generate</div>show QR</div><div class="delete"><button data-vmess="'''+ user_info[5] +'''" onclick="delete_user(this.getAttribute('data-vmess'));">Delete</button></div><hr>'''

                        elif float(used_data) > float(max_data) or time_left < 0:
                            if user_info[0][-1] != "e":
                                disable_enable(user_info[1], "disable")
                            text2 = text2 + '''<div class="name disable">'''+ str(user_info[2]) +'''<div style="background-color: #ffffff80;float: left;padding: 0 20px;">'''+connected_users_to_this_port+'''</div></div><div class="status disable" style="font-family: tahoma;">disable</div><div class="data-usage disable"><div style="float: left;border-style: none;padding: 0px;">edit</div>'''+ str(int(used_data)/1000) + '''GB | ''' + str(float(max_data)/1000) +'''GB</div><div class="date disable">'''+ str(round(time_left, 1)) +''' Days</div><div class="vmess-link disable" data-vmess="'''+ user_info[5] +'''" onclick="copyToClipboard(this.getAttribute('data-vmess'));"><div style="text-align: center; width: 100%;">click to copy</div>'''+ user_info[5] +'''</div><div class="qrcode disable" data-vmess="'''+ user_info[5] +'''" onclick="makeCode(this.getAttribute('data-vmess'));"><div style="text-align: center; width: 100%;">Generate</div>show QR</div><div class="delete"><button data-vmess="'''+ user_info[5] +'''" onclick="delete_user(this.getAttribute('data-vmess'));">Delete</button></div><hr>'''

                    text1 = '''<div id="list-continer"><div style="width: 80px;right: 5px;height: 50px;position: fixed;background-color: #aaf4a8;padding: 20px 30px 10px;text-align: left;">'''+str(all_connected)+'''</div>'''
                    await websocket.send(text1 + text2 + "</div>" + '''<div style="position: fixed; display: inline-block; right: 2%; top: 20px;"><button onclick="logout();">logout</button></div><div style="position: fixed; display: inline-block; right: 2%; top: 60px;"><button onclick="add_user();">add user +</button></div>''')
                else:
                    await websocket.send("username or password not found ...")
            elif message.startswith("<-login"):
                user_info = message.replace("<-login", "").split("/*/|")
                admin_id = check_admin(str(user_info[0]), str(user_info[1]))
                if admin_id != False:
                    if user_info[2] != "" and user_info[3] != "" and user_info[4] != "":
                        current_GMT = time.gmtime()
                        current_time = calendar.timegm(current_GMT)
                        add_user("156.255.1.217", random.randint(1000, 65400), admin_id, (float(user_info[3])*1000), (int(current_time)+(int(user_info[4])*86400)), str(user_info[2]))
                        await websocket.send("successful")
            elif message.startswith("<-delete"):
                user_info = message.replace("<-delete", "").split("/*/|")
                admin_id = check_admin(str(user_info[0]), str(user_info[1]))
                if admin_id != False:
                    print(admin_id)
                    port = link_to_port(user_info[2])
                    print(type(port))
                    print(port)
                    delete_user("156.255.1.217", int(port))
                    await websocket.send("user deleted")



    except websockets.exceptions.ConnectionClosed as e:
        all_clients.remove(websocket)
        print('A client just disconnected')








'''def func1():
    while True:
        for client in all_clients:
            client.send("hello")
    time.sleep(5)



if __name__ == '__main__':
    Thread(target = func1).start()'''


async def main():
    async with websockets.serve(echo, "156.255.1.217", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())



