import os
import subprocess
import random


def add_admin(username, password):
    file = open("admins.conf", "r")
    content = file.read()
    file.close()
    if not (username + "|" + password + "|") in content:
        id = str(random.randint(1000000000, 9999999999))
        file = open("admins.conf", "a")
        file.write(username + "|" + password + "|" + id + "\n")
        file.close()
        print("user added ...")
        return True
    else:
        print("username and password are used befor ...")
        return False


def check_admin(username, password):
    file = open("admins.conf", "r")
    content = file.read()
    file.close()
    all_lines = content.splitlines()
    for i in all_lines:
        if (username + "|" + password + "|") in i:
            id = i.split("|")[2]
            return id
    return False


#print(str(check_admin("admi", "1234qwe")))

def users_list(id):
    users_list = []
    file = open("users.conf", "r")
    content = file.read()
    file.close()
    all_users = content.splitlines()
    for i in all_users:
        if ("|" + str(id) + "|") in i:
            users_list.append(i)
    return users_list




#print(users_list(1920631160))


