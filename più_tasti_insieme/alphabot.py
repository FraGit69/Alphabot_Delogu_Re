import socket
#  import alphaLib

tastiConcessi = ['w', 'a', 's', 'd']
alphabot_address = ("127.0.0.1", 34512)

alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alphabot_tcp.bind(alphabot_address)
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

# alpha = alphaLib.AlphaBot()
try:
    while True:
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")
        while True:
            messaggio = client.recv(4096).decode('utf-8')
            print(messaggio)
            messaggio = messaggio.split(",")
            print(messaggio)

except KeyboardInterrupt:
    print("Server interrotto manualmente.")
finally:
    alphabot_tcp.close()
    print("Server chiuso.")


