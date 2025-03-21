import socket
import alphaLib

tastiConcessi = ['w', 'a', 's', 'd']
alphabot_address = ("localhost", 34512)

alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alphabot_tcp.bind(alphabot_address)
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

alpha = alphaLib.AlphaBot()
try:
    while True:
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")
        while True:
            messaggio = client.recv(4096).decode('utf-8')
            if messaggio == "end":
                client.close()
                break
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


                if left >100 or left <-100:
                    left /=10
                if right >100 or left <-100:
                    right/=10
                alpha.setMotor(right, left)
                print(right, left)
        print(f"connessione chiusa con {address}")
        alpha.stop()

except KeyboardInterrupt:
    print("Server interrotto manualmente.")
finally:
    alphabot_tcp.close()
    print("Server chiuso.")


