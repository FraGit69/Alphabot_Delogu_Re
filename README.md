# Alphabot Movement Control via TCP Socket

### Autori
- **Francesco Re**
- **Davide Delogu**

## Descrizione del progetto

Questo progetto si concentra sul controllo del movimento di un drone terrestre, l'Alphabot, utilizzando una connessione **socket TCP**. L'obiettivo è quello di inviare comandi di movimento attraverso la rete per guidare l'Alphabot in diverse direzioni.
Progressi:
1. Comunicazione tra due pc per testare un server e un client tcp con socket in python, dove il server in ascolto mandasse un messaggio al server e questo gli invii una risposta di conseguenza.
2. Sviluppo di un programma di EventListener per poter vedere quali tasti sono premuti
3. Unione dei due precedenti
4. Implementazione del programma utilizzando la libreria alphaLib.py per la gestione dei motori.

## Funzionalità principali

- Controllo remoto del movimento dell'Alphabot tramite comandi TCP.
- Movimenti disponibili: avanti, indietro, sinistra, destra, fermarsi.
- Connessione stabile e affidabile grazie al protocollo TCP.
  
## Struttura del Progetto

Il progetto è composto da due parti principali:

1. [**Server**](https://github.com/FraGit69/Alphabot_Delogu_Re/blob/master/alphabot.py): che riceve i comandi di movimento dal client e li inoltra all'Alphabot, che quindi risiede all'interno del alphabot insieme alla libreria alphaLib.py.
2. [**Client**](https://github.com/FraGit69/Alphabot_Delogu_Re/blob/master/pc.py): che invia i comandi al server tramite la connessione TCP.

## Tecnologie Utilizzate

- **Socket TCP** per la comunicazione tra client e server.
- **Python** per l'implementazione della logica di controllo e la gestione dei socket.
- **Raspberry Pi** come piattaforma di controllo per l'Alphabot.

## Requisiti

- **Python 3.x**
- **Alphabot**
- **Raspberry Pi** con sistema operativo configurato [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/)
- Librerie Python:
  - `socket` (inclusa di default in Python)
  - `alphaLib` (inclusa nella [repository](https://github.com/FraGit69/Alphabot_Delogu_Re/blob/master/alphaLib.py))
  - `pynput` (da installare)

## Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-username/alphabot-tcp.git
   cd alphabot-tcp
   ```
2. Installa la libreria pynput
   ```bash
   pip install pynput
   ```
3.Configura il server sul Raspberry Pi per ricevere comandi TCP e inviarli all'Alphabot.
  Assicurati che il server e il client abbiano l'indirizzo IP dell'alphabot, che assumerà la funzione del server, e che se non presenti non funzioneranno.

## Esecuzione

1. Collegati sull'alphabot in ssh e esegui il codice python
  ```bash
  python3 alphabot.py
  ```
2. Quando sarà avviato il server TCP, che si nota da terminale ssh con la stringa `"Server TCP in ascolto..."`, esegui sul tuo computer il file del client `pc.py`:
  ```bash
  python3 pc.py
  ```
