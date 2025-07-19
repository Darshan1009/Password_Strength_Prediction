from flask import Flask, render_template, request, session, jsonify, send_file
import pickle
import numpy as np
import random
import string
import json
import os
from datetime import datetime
from io import BytesIO

# Load the trained model and vectorizer
with open('model.pkl', 'rb') as f:
    clf = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

app = Flask(__name__)
# Use environment variable for secret key, fallback for dev only
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_change_me')

def predict_password_strength(password):
    sample_array = np.array([password])
    sample_matrix = vectorizer.transform(sample_array)
    length_pass = len(password)
    length_normalized_lowercase = len([char for char in password if char.islower()]) / len(password) if len(password) > 0 else 0
    extra_features = np.array([[length_pass, length_normalized_lowercase]])
    new_matrix = np.concatenate((sample_matrix.toarray(), extra_features), axis=1)
    result = clf.predict(new_matrix)
    if result == 0:
        return "Password is weak"
    elif result == 1:
        return "Password is normal"
    else:
        return "Password is strong"

def password_details(password):
    return {
        "Length": len(password),
        "Uppercase": sum(1 for c in password if c.isupper()),
        "Lowercase": sum(1 for c in password if c.islower()),
        "Digits": sum(1 for c in password if c.isdigit()),
        "Symbols": sum(1 for c in password if not c.isalnum())
    }

def suggest_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    chars = ""
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    
    if not chars:
        chars = string.ascii_letters + string.digits + string.punctuation
    
    attempts = 0
    while attempts < 100:  # Prevent infinite loop
        pwd = ''.join(random.choice(chars) for _ in range(length))
        
        # Check if password meets the requirements
        has_upper = not use_uppercase or any(c.isupper() for c in pwd)
        has_lower = not use_lowercase or any(c.islower() for c in pwd)
        has_digit = not use_digits or any(c.isdigit() for c in pwd)
        has_symbol = not use_symbols or any(not c.isalnum() for c in pwd)
        
        if has_upper and has_lower and has_digit and has_symbol:
            return pwd
        
        attempts += 1
    
    # If we can't generate a password with all requirements, return one with available chars
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    details = None
    suggestion = None
    password = ""
    if 'history' not in session:
        session['history'] = []
    if request.method == 'POST':
        password = request.form['password']
        result = predict_password_strength(password)
        details = password_details(password)
        # Save to history (max 10)
        history = session['history']
        history.insert(0, {
            "password": password, 
            "result": result, 
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": details
        })
        session['history'] = history[:10]
        if "weak" in result.lower():
            suggestion = suggest_password()
    return render_template('index.html', result=result, details=details, suggestion=suggestion, history=session.get('history', []), password=password)

@app.route('/history')
def history():
    return render_template('history.html', history=session.get('history', []))

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    length = data.get('length', 12)
    use_uppercase = data.get('use_uppercase', True)
    use_lowercase = data.get('use_lowercase', True)
    use_digits = data.get('use_digits', True)
    use_symbols = data.get('use_symbols', True)
    
    password = suggest_password(length, use_uppercase, use_lowercase, use_digits, use_symbols)
    result = predict_password_strength(password)
    details = password_details(password)
    
    return jsonify({
        "password": password,
        "result": result,
        "details": details
    })

@app.route('/download_history')
def download_history():
    history = session.get('history', [])
    
    # Create CSV content
    csv_content = "Password,Strength,Length,Uppercase,Lowercase,Digits,Symbols,Timestamp\n"
    for entry in history:
        details = entry.get('details', {})
        csv_content += f'"{entry["password"]}","{entry["result"]}",{details.get("Length", 0)},{details.get("Uppercase", 0)},{details.get("Lowercase", 0)},{details.get("Digits", 0)},{details.get("Symbols", 0)},"{entry.get("timestamp", "")}"\n'
    
    # Create BytesIO object
    output = BytesIO()
    output.write(csv_content.encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'password_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['history'] = []
    return jsonify({"success": True})

# API endpoint for programmatic access
@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.json
    password = data.get('password', '')
    result = predict_password_strength(password)
    details = password_details(password)
    return {"result": result, "details": details}

if __name__ == '__main__':
    app.run(debug=True) 