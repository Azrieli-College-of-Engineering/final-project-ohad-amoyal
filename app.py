from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = "super-secret-key" # המפתח שהשרת אמור להשתמש בו

@app.route('/login', methods=['POST'])
def login():
    # מדמה התחברות מוצלחת של משתמש רגיל
    user_data = {"user": "ohad", "role": "user"}
    token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
    return jsonify({"token": token})

@app.route('/admin', methods=['GET'])
def admin_only():
    token = request.headers.get('Authorization')
    if not token:
        return "Missing token", 401
    
    try:
        # כאן נמצאת החולשה: השרת לא מגביל את האלגוריתם ל-HS256 בלבד
        # מה שמאפשר לתוקף לשלוח טוקן עם אלגוריתם 'none'
        decoded = jwt.decode(token, options={"verify_signature": False}) 
        
        if decoded.get("role") == "admin":
            return "Welcome Ohad! You have Admin access."
        else:
            return "Access denied: Regular users only.", 403
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(port=5000)