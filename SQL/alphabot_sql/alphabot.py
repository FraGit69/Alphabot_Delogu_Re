import socket
import sqlite3 as sql
# import alphaLib
import time as t

tastiConcessi = ['w', 'a', 's', 'd']
alphabot_address = ("localhost", 34512)

alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alphabot_tcp.bind(alphabot_address)
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

conn = sql.connect("./movimenti.db")
cur = conn.cursor()
cur.execute("""SELECT *
FROM MOVIMENTO""")
movimenti = {key:mov for key, mov in cur.fetchall()}
print(movimenti)

# alpha = alphaLib.AlphaBot()
try:
    while True:
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")
        while True:
            messaggio = client.recv(4096).decode('utf-8')
            if messaggio == "end":
                client.send("end".encode('utf-8'))
                alphabot_tcp.close()
                continue
            
            messaggio = messaggio.split(",")
            if len(messaggio)==2:
                try:
                    right = int(messaggio[0])
                except:
                    right = eval(messaggio[0])

                try:
                    left = int(messaggio[1])
                except:
                    left = eval(messaggio[1])

                # alpha.setMotor(right, left)
                print(f"dx {right} sx {left}")
            else:
                movimento = movimenti[messaggio[0]].split(',')
                for mov in movimento:
                    dir, temp = mov.split(':')
                    print(dir)
                    # if dir == 'W':
                    #     alpha.forward()
                    # elif dir == 'S':
                    #     alpha.backward()
                    # elif dir == 'D':
                    #     alpha.right()
                        
                    # elif dir == 'A':
                    #     alpha.left()
                    t.sleep(int(temp)) 
                client.send("finish".encode('utf-8')) 

                

except KeyboardInterrupt:
    print("Server interrotto manualmente.")
finally:
    alphabot_tcp.close()
    print("Server chiuso.")


