"""
JWT: JSON Web Tokens

This python code implements an authentication wrapper using JWT

Questions: 
1. Identify potential security issues in JWT and database interactions.
2. Describe all attack scenarios in as much detail as possible using the security issues reported.
3. Provide fixes for all the identified issues.

How: 
Research on common SQL and JWT issues and bypasses.
"""

from flask import Flask, request, make_response
import jwt
import base64
import json
import sqlite3
import logging
from utils.db_utils import DatabaseUtils
from utils.file_storage import FileStorage
import os
import urllib.parse
import datetime
from datetime import UTC
import html

app = Flask(__name__)

#SECRET_KEY = "secret_key"
SECRET_KEY=os.getenv("SECRET_KEY")
#logging.info(f"SECRET_KEY: {SECRET_KEY}")

logging.basicConfig(level=logging.INFO)
db = DatabaseUtils()
fs = FileStorage()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _init_app():
    db.update_data("DROP TABLE IF EXISTS users;")
    db.update_data('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            privilege INTEGER
                        );''')
    db.update_data("INSERT INTO users (username, password, privilege) VALUES ('user1', 'password1', 0)")
    db.update_data("INSERT INTO users (username, password, privilege) VALUES ('admin1', 'adminpassword1', 1)")
        

def _check_login():
    auth_token = request.cookies.get('token', None)
    if not auth_token:
        raise ValueError("Missing token cookie")
    try:
        # Decode JWT token
        token = auth_token[len(auth_token)//2:] + auth_token[:len(auth_token)//2]
        decoded_token = base64.urlsafe_b64decode(token.encode()).decode()
        data = jwt.decode(json.loads(decoded_token), SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        raise ValueError("Token is invalid")
    return data


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    logging.info(f"username: {username}, password: {password}")
    rows = db.fetch_data("SELECT * FROM users WHERE username=? AND password=?", (username, password))

    if len(rows) != 1:
        return "Invalid credentials", 401
    
    token = jwt.encode({ "username": username, "iat": datetime.datetime.now(UTC), "exp": datetime.datetime.now(UTC) + datetime.timedelta(hours=1) }, SECRET_KEY, algorithm="HS256")
    encoded_token = json.dumps(token).encode()
    obfuscate1 = base64.urlsafe_b64encode(encoded_token).decode()
    obfuscate3 = obfuscate1[len(obfuscate1)//2:] + obfuscate1[:len(obfuscate1)//2]
    # Everyone knows how to read JWT tokens these days. The team decided to obfuscate it as a pickle and
    # some fancy tricks so nobody can tell we're using JWT and can't exploit us using common JWT exploits :D
    # Devs knowing some security sure is useful! :P

    res = make_response()
    res.set_cookie("token", value=obfuscate3, httponly=True, secure=True, samesite='Strict')
    res.set_cookie("admin", value='true' if rows[0][-1]==1 else 'false', httponly=True, secure=True, samesite='Strict')

    return res


@app.route("/file", methods=["GET", "POST", "DELETE"])
def store_file():
    """
    Only admins can upload/delete files.
    All users can read files.
    """
    try:
        data = _check_login()
    except:
        return "Not logged in", 401

    # Fetch username from verified JWT token data
    username = data.get("username")

    # Verify privilege directly from the database
    rows = db.fetch_data("SELECT privilege FROM users WHERE username=?", (username,))

    # checking both db and cookie for admin status
    db_is_admin = rows and rows[0][0] == 1
    cookie_is_admin = request.cookies.get('admin', 'false') == 'true'

    is_admin = db_is_admin and cookie_is_admin


    if request.method == 'GET':
        filename = request.args.get('filename')
        return fs.get(filename)
    elif request.method == 'POST':
        if not is_admin: return "Need admin access", 403
        uploaded_files = request.files
        logging.error(uploaded_files)
        for f in uploaded_files:
            raw_filename = uploaded_files[f].filename
            decoded_filename = urllib.parse.unquote(raw_filename)
            safe_filename = decoded_filename.replace('\n', '').replace('\r', '')
            if not allowed_file(safe_filename):
                return "Invalid file type, only 'jpeg, jpg, png, pdf, gif, txt' are allowed", 400
            
            fs.store(safe_filename, uploaded_files[f].read())
            logging.info(f'Uploaded filename: {safe_filename}')
        return "Files uploaded successfully"
    elif request.method == 'DELETE':
        if not is_admin: return "Need admin access", 403
        filename = request.args.get('filename')
        sanitized_filename = html.escape(filename)  # Escapes HTML characters
        if fs.delete(sanitized_filename):
            return f"{sanitized_filename} deleted successfully", 200
        else:
            return f"{sanitized_filename} not found", 404
    else:
        return "Method not implemented", 405


if __name__ == "__main__":
    _init_app()
    app.run(host='0.0.0.0', debug=True, port=9090)
