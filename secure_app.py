# secure_app.py
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = "super-secret-key"

@app.route('/login', methods=['POST'])
def login():
    user_data = {"user": "ohad", "role": "user"}
    token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
    return jsonify({"token": token})

@app.route('/admin', methods=['GET'])
def admin_only():
    token = request.headers.get('Authorization')
    if not token:
        return "Missing token", 401
    
    try:
        # ההגנה: הוספת algorithms=['HS256'] מכריחה את השרת לבדוק חתימה
        # אם תוקף ישלח אלגוריתם 'none', השרת יזרוק שגיאה
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        if decoded.get("role") == "admin":
            return "Welcome Ohad! You have Admin access."
        else:
            return "Access denied: Regular users only.", 403
    except jwt.InvalidTokenError:
        return "Invalid Token - Attack Detected!", 401

if __name__ == '__main__':
    app.run(port=5001)