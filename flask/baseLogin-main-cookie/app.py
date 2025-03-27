from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import alphaLib as ab

app = Flask(__name__)
app.secret_key = "secret_key"  # Chiave segreta necessaria per le sessioni e i messaggi flash
alpha = ab.AlphaBot()

# Funzione per inizializzare il database e creare la tabella utenti se non esiste
def init_db():
    with sqlite3.connect("utenti.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()
        print("Database inizializzato.")  # Messaggio di debug


# Rotta per il login
@app.route("/", methods=["GET", "POST"])
def login():
    nomeC = request.cookies.get("mycookie")  # Controlla se esiste un cookie salvato
    if nomeC:
        return redirect(url_for("alphabot"))  # Se il cookie esiste, reindirizza al telecomando

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print(f"Ricevuto username: {username}, password: {password}")  # Debug

        # Controllo credenziali nel database
        with sqlite3.connect("utenti.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM utenti WHERE username = ?", (username,))
            user = cursor.fetchone()
            print(f"Risultato query: {user}")  # Debug

        if user is not None:
            if check_password_hash(user[0], password):  # Verifica l'hash della password
                risposta = redirect(url_for("alphabot", username=username))
                risposta.set_cookie("mycookie", username, max_age=60*60*24)  # Imposta un cookie per ricordare l'utente
                return risposta
        else:
            return render_template("login.html", alert="Utente non trovato")

    return render_template('login.html')


# Rotta per il controllo dell'AlphaBot
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
        # Qui puoi gestire l'azione ricevuta (ad esempio, inviare comandi all'AlphaBot)
        print(f"Azione ricevuta: {action}")
        return jsonify({"status": "success", "action": action})
    return render_template('index.html')

# Rotta per la creazione di un nuovo account
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Cripta la password

        try:
            # Inserisce il nuovo utente nel database
            with sqlite3.connect("utenti.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                print(f"Utente {username} salvato nel database.")  # Debug
                return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("create_account.html", alert="Utente già esistente")

    return render_template('create_account.html')


# Rotta per il logout
@app.route("/logout")
def logout():
    session.pop("username", None)  # Rimuove l'username dalla sessione
    print("Utente disconnesso.")  # Debug

    risposta = make_response(redirect(url_for("login")))
    risposta.delete_cookie("mycookie")  # Elimina il cookie di autenticazione
    return risposta


if __name__ == "__main__":
    init_db()  # Inizializza il database all'avvio dell'applicazione
    app.run(debug=True, host="0.0.0.0", port=4444)
