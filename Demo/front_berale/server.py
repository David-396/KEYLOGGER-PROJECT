from flask import Flask, request, redirect, jsonify, send_from_directory

app = Flask(__name__, static_folder='public', static_url_path='')

# נתוני הדמה – 5 מחשבים
computers = [
    {"id": 1, "name": "מחשב 1", "specs": "CPU: i5, RAM: 8GB, OS: Windows 10"},
    {"id": 2, "name": "מחשב 2", "specs": "CPU: i7, RAM: 16GB, OS: Windows 11"},
    {"id": 3, "name": "מחשב 3", "specs": "CPU: Ryzen 5, RAM: 8GB, OS: Linux"},
    {"id": 4, "name": "מחשב 4", "specs": "CPU: Ryzen 7, RAM: 16GB, OS: macOS"},
    {"id": 5, "name": "מחשב 5", "specs": "CPU: i3, RAM: 4GB, OS: Windows 10"}
]

# נתינת דף הכניסה כברירת מחדל
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'login.html')

# טיפול בכניסת משתמש – אם השדות קיימים, נעביר לדף ניתוח
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        return redirect('/analysis.html')
    else:
        return 'הכניסה נכשלה', 400

# API להחזרת רשימת המחשבים
@app.route('/api/computers', methods=['GET'])
def get_computers():
    return jsonify(computers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
