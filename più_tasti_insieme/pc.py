import socket as s
from pynput import keyboard

keys_granted = ["w", "a", "s", "d"]
keys_pressed = []
left = 0
right = 0

def client():
    alphabot_address = ("127.0.0.1", 34512)
    try:
        # Connessione al server Alphabot
        client_tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
        client_tcp.connect(alphabot_address)
        print("Connected to Alphabot")
        # Listener per la tastiera
        with keyboard.Listener(on_press=lambda key: on_press(key, client_tcp),
                               on_release=lambda key: on_release(key, client_tcp)) as listener:
            listener.join()  # Mantiene il listener attivo finché non viene fermato
    except ConnectionRefusedError:
        print("Connection to Alphabot refused")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client_tcp' in locals():
            client_tcp.close()
            print("Connection closed.")

def on_press(key, client_tcp):
    try:
        if key.char in keys_granted and key.char not in keys_pressed:
            keys_pressed.append(key.char)
            global left, right
            if key.char == "w":
                right += 50
                left -= 50
            elif key.char == "s":
                right -= 50
                left += 50
            elif key.char == "a":
                right += 30
            elif key.char == "d":
                left -= 30
            print(f"{left},{right}")
            client_tcp.send(f"{left},{right}".encode("utf-8"))
    except AttributeError:
        pass  # Ignora tasti speciali come Ctrl, Alt, ecc.

def on_release(key, client_tcp):
    try:
        if key.char in keys_granted and key.char in keys_pressed:
            keys_pressed.remove(key.char)
            global left, right
            if key.char == "w":
                right -= 50
                left += 50
            elif key.char == "s":
                right += 50
                left -= 50
            elif key.char == "a":
                right -= 30
            elif key.char == "d":
                left += 30
            print(f"{left},{right}")
            client_tcp.send(f"{left},{right}".encode("utf-8"))
    except AttributeError:
        pass  # Ignora tasti speciali come Ctrl, Alt, ecc.

if __name__ == "__main__":
    client()
