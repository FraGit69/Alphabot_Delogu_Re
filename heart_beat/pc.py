import socket as s
from pynput import keyboard
import threading as t
import time

alphabot_address = ("192.168.1.136", 34512)
keys_granted = ["w", "a", "s", "d"]
keys_pressed = []
left = 0
right = 0
connection = False
ping_started = False

def client():
    global connection
    try:
        # Connessione al server Alphabot
        client_tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
        client_tcp.connect(alphabot_address)
        connection = True
        print("Connected to Alphabot")
        num = int(client_tcp.recv(4096).decode("utf-8"))
        ping = t.Thread(target=handle_ping, args=(num,))
        ping.start()
        # Listener per la tastiera
        with keyboard.Listener(on_press=lambda key: on_press(key, client_tcp),
                               on_release=lambda key: on_release(key, client_tcp)) as listener:
            listener.join()  # Mantiene il listener attivo finché non viene fermato
        
    except ConnectionRefusedError:
        print("Connection to Alphabot refused")
    except Exception as e:
        print(f"An error occurred: {e}")

    connection = False
    if ping_started:
        ping.join()
    client_tcp.close() 
    print("Connection closed.")

def on_press(key, client_tcp):
    try:
        if key.char in keys_granted and key.char not in keys_pressed:
            keys_pressed.append(key.char)
            global left, right
            if key.char == "w":
                if 'a' in keys_pressed and 's' not in keys_pressed and right<0:
                    right+=60
                if 'd' in keys_pressed and 's' not in keys_pressed and left >0:
                    left-=60

                right += 50
                left -= 50
            elif key.char == "s":
                if 'a' in keys_pressed and 'w' not in keys_pressed and right>0:
                    right-=60
                if 'd' in keys_pressed  and 'w' not in keys_pressed and left<0:
                    left+=60

                right -= 50
                left += 50

            elif key.char == "a":
                right+=30
                if "s" in keys_pressed and "w" not in keys_pressed:
                    right-=60
            elif key.char == "d":
                left-=30
                if "s" in keys_pressed and "w" not in keys_pressed:
                    left+=60
            client_tcp.send(f"{-right},{-left}".encode("utf-8"))
            
    except AttributeError:
        if key == keyboard.Key.esc:
            client_tcp.send("end".encode("utf-8"))
            return False
        if key == keyboard.Key.shift:
            client_tcp.send(f"-100,100".encode("utf-8"))

def on_release(key, client_tcp):
    global left, right
    try:
        if key.char in keys_granted and key.char in keys_pressed:
            keys_pressed.remove(key.char)
            if key.char == "w":
                right -= 50
                left += 50
            elif key.char == "s":
                right += 50
                left -= 50
            elif key.char == "a":
                if right >0:
                    right-=30
                else:
                    right+=30
            elif key.char == "d":
                if left >0:
                    left-=30
                else:
                    left+=30
            client_tcp.send(f"{right},{left}".encode("utf-8"))
    except AttributeError:
        if key == keyboard.Key.shift:
            client_tcp.send(f"0,0".encode("utf-8"))

def handle_ping(num):
    global ping_started
    global connection
    ping_started = True
    alphabot_address_ping = (alphabot_address[0], alphabot_address[1]+num)
    ping_udp = s.socket(s.AF_INET, s.SOCK_DGRAM)
    ping_udp.connect(alphabot_address_ping)
    print("connesso ping!")
    cont=0
    while connection:
        time.sleep(1)
        ping_udp.send(f"{cont}".encode("utf-8"))
        cont+=1
    
    ping_udp.close()

if __name__ == "__main__":
    client()
