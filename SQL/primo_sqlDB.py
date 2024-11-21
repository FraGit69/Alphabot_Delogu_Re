import sqlite3

# se il file del db non esiste lo crea
conn = sqlite3.connect('esempio.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS comandi (
    tasto TEXT PRIMARY KEY,
    comando TEXT NOT NULL);
''')


comandi = [
    ('p', 'Rossi'),
    ('r', 'Bianchi'),
    ('t', 'Verdi')
]

cur.executemany('''
    INSERT INTO comandi (Tasto, Comando)
    VALUES (?, ?)
''', comandi)

conn.commit()