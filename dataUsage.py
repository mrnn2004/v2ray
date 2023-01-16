import subprocess



def data_usage(port):
    command = 'iptables -n -L -v | grep "Chain INPUT\|:'+ str(port) +'\|Chain OUTPUT"'
    subprocess1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess1.stdout.read()
    line_list = subprocess_return.decode("utf-8").splitlines()

    download = line_list[3].split()[1]
    upload = line_list[1].split()[1]


    if download[-1] == "G":
        download = int(download[:-1])*1000
    elif download[-1] == "M":
        download = int(download[:-1])
    elif download[-1] == "K":
        if int(download[:-1]) > 1000:
            download = int(int(download[:-1])/1000)
        else:
            download = 0
    else:
        download = 0

    if upload[-1] == "G":
        upload = int(upload[:-1])*1000
    elif upload[-1] == "M":
        upload = int(upload[:-1])
    elif upload[-1] == "K":
        if int(upload[:-1]) > 1000:
            upload = int(int(upload[:-1])/1000)
        else:
            upload = 0
    else:
        upload = 0


    return str(download) + ":" + str(upload)
        

#print(data_usage(8888))

