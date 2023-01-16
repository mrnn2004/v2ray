from dataUsage import *
from usersManage import disable_enable, get_date
import time
import calendar


while True:
    file = open("users.conf", "r")
    content = file.read()
    file.close()
    if content != "":
        users_list = content.splitlines()
        for i in users_list:
            user_info = i.split("|")
            used_data = data_usage(user_info[1]).split(":")
            used_data = (int(used_data[0]) + int(used_data[1]))
            max_data = int(user_info[3])
            current_GMT = time.gmtime()
            current_time = calendar.timegm(current_GMT)
            ex_time = int(get_date(user_info[1]))
            time_left = (ex_time - current_time)/86400


            if used_data <= max_data and time_left > 0:
                if user_info[0][-1] != "a":
                    disable_enable(user_info[1], "enable")

            elif used_data > max_data or time_left < 0:
                if user_info[0][-1] != "e":
                    disable_enable(user_info[1], "disable")
    else:
        print("file is empty")
    time.sleep(1)



