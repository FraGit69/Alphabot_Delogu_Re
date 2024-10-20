import socket
from pynput import keyboard

tastiConcessi = ["w", "a", "s", "d"]
tastiPremuti = list()
# Definizione dell'indirizzo del server
server_tcp_address = ("192.168.1.129", 34512)

# Creazione del socket TCP del client
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(server_tcp_address)

def gestione_congestione_on_press(key):
    if key not in tastiPremuti:
        tastiPremuti.append(key)
        invia_comando(key)

def gestione_congestione_on_release(key):
    if key in tastiPremuti:
        tastiPremuti.pop(key)

# Funzione per inviare il comando al server
def invia_comando(func, power=50):
    messaggio = f"{func}"
    client_tcp.send(messaggio.encode('utf-8'))
# Funzione per gestire i tasti premuti
def on_press(key):
    try:
        if key.char in tastiConcessi:
            gestione_congestione_on_press(key.char)
            invia_comando("stop")
    except AttributeError:
        if key == keyboard.Key.esc:
            return False

def on_release(key):
    try:
        if key.char in tastiConcessi:
            gestione_congestione_on_release(key.char)
    except AttributeError:
        pass

# Listener per i tasti premuti
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



# Chiudi la connessione TCP
client_tcp.close()