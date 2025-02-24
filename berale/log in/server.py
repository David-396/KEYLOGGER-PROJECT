from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # טיפול אוטומטי ב-CORS

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

if __name__ == '__main__':
    app.run(debug=True)
