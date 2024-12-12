import socket as s
# import alphaLib
import threading as t
import time

TIMEOUT_CLIENT = 2 # sec

tastiConcessi = ['w', 'a', 's', 'd']
alphabot_address = ("localhost", 34512)
connection_active = False

def handle_ping(num):
    global connection_active
    alphabot_address_ping = (alphabot_address[0], alphabot_address[1]+num)
    ping_udp = s.socket(s.AF_INET, s.SOCK_DGRAM)
    ping_udp.bind(alphabot_address_ping)
    last_ping = -1
    while connection_active:
        try:
            data, addr = ping_udp.recvfrom(1024)
            ping_message = int(data.decode("utf-8"))
            
            if ping_message >last_ping:
                last_ping = ping_message
            else:
                connection_active = False
                break
        except s.timeout:
            print("Timeout nell'heartbeat")
            connection_active = False
        except Exception as e:
            print(f"Errore nell'heartbeat: {e}")
            connection_active = False

    ping_udp.close()


def alphabot():
    global connection_active
    alphabot_tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
    alphabot_tcp.bind(alphabot_address)
    alphabot_tcp.listen(1)
    print("Server AlphaBot in ascolto...")



    # alpha = alphaLib.AlphaBot()
    try:
        while True:
            client, address = alphabot_tcp.accept()
            connection_active = True
            num = 1
            client.send(f"{num}".encode("utf-8"))
            thread_ping = t.Thread(target=handle_ping, args=(num,))
            thread_ping.start()
            print(f"Connessione accettata da {address}")
            while connection_active:
                messaggio = client.recv(4096).decode('utf-8')
                if messaggio == "end":
                    connection_active=False
                    client.close()
                else:
                    messaggio = messaggio.split(",")
                    try:
                        right = int(messaggio[0])
                    except:
                        right = eval(messaggio[0])

                    try:
                        left = int(messaggio[1])
                    except:
                        left = eval(messaggio[1])

                    # alpha.setMotor(right, left)
                    print(right, left)
            thread_ping.join()
            print(f"connessione chiusa con {address}")

    except KeyboardInterrupt:
        print("Server interrotto manualmente.")
    
    alphabot_tcp.close()
    # alpha.stop()
    print("Server chiuso.")

if __name__ == "__main__":
    alphabot()


