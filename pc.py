import socket
from pynput import keyboard

# Definizione dell'indirizzo del server
server_tcp_address = ("192.168.1.129", 34512)

# Creazione del socket TCP del client
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(server_tcp_address)

# Funzione per inviare il comando al server
def invia_comando(func, power=50):
    messaggio = f"{func}"
    client_tcp.send(messaggio.encode('utf-8'))

# Funzione per gestire i tasti premuti
def on_press(key):
    try:
        if key.char == 'w':
            invia_comando('w')  # Avanti
        elif key.char == 's':
            invia_comando('s')  # Indietro
        elif key.char == 'd':
            invia_comando('d')  # Destra
        elif key.char == 'a':
            invia_comando('a')  # Sinistrawq
        elif key.char == 'q':
            invia_comando('stop')  # Stop
    except AttributeError:
        pass

def on_release(key):
    try:
        if key.char in ["w", "a", "s", "d"]:
            invia_comando("stop")
    except AttributeError:
        pass

# Listener per i tasti premuti
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



# Chiudi la connessione TCP
client_tcp.close()
