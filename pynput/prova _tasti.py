import socket as s
from pynput import keyboard

keys_granted = ["w", "a", "s", "d"]
keys_pressed = []
left = 0
right = 0


def client():
    # Listener per la tastiera
    with keyboard.Listener(on_press=lambda key: on_press(key),
                            on_release=lambda key: on_release(key)) as listener:
        listener.join()  # Mantiene il listener attivo finché non viene fermato

def on_press(key):
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
    except AttributeError:
        pass  # Ignora tasti speciali come Ctrl, Alt, ecc.

def on_release(key):
    print(key.char in keys_granted and key.char not in keys_pressed)
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
    except AttributeError:
        pass  # Ignora tasti speciali come Ctrl, Alt, ecc.

if __name__ == "__main__":
    client()
