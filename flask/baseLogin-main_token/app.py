from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3 as sql
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import alphaLib as ab

app = Flask(__name__)
app.secret_key = "secret_key"  # Chiave segreta necessaria per le sessioni e i messaggi flash
alpha = ab.AlphaBot()

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.now() + datetime.timedelta(days=1)  # Scadenza in 1 giorno
    }
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        return None  # Token scaduto
    except jwt.InvalidTokenError:
        return None  # Token non valido


@app.route("/alphabot", methods=['GET', 'POST'])
def alphabot():
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        if action == 'right':
            alpha.right()
        if action == 'left':
            alpha.left()
        if action == 'forward':
            alpha.forward()
        if action == 'backward':
            alpha.backward()
        if action == 'sprint':
            alpha.setMotor(80, 80)
        if action == 'stop':
            alpha.stop()
       # Qui puoi gestire l'azione ricevuta (ad esempio, inviare comandi all'AlphaBot)
        print(f"Azione ricevuta: {action}")
        return jsonify({"status": "success", "action": action})
    return render_template('index.html')



@app.route("/", methods=["GET", "POST"])
def login():
    if request.cookies.get('token'):
        return redirect(url_for("alphabot"))
    else: 
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            return validate(email, password)
        return render_template("login.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sql.connect("users.db")
        cur = conn.cursor()
        cur.execute(f"""SELECT 1
                        FROM users
                        WHERE email LIKE '{email}'""")
        user = cur.fetchone()
        if user==None:
            cur.execute(f"""INSERT INTO users (email, password)
                            VALUES ('{email}', '{generate_password_hash(password)}')""")
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        else:
            # utente già esistente
            pass
    return render_template("create_account.html")


@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.set_cookie('token', '', expires=0)
    return resp

def validate(username, password):
    conn = sql.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"""SELECT users.password FROM users WHERE email = ?""", (username,))
    pswd = cur.fetchone()
    
    if pswd and check_password_hash(pswd[0], password):
        token = generate_token(username)
        resp = redirect(url_for("alphabot"))
        resp.set_cookie('token', token, httponly=True)  # Memorizza il token nel cookie
        return resp
    
    return render_template("login.html", alert="Invalid credentials")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4444)
