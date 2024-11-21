from pynput import keyboard

def on_press(key):
    """Funzione chiamata quando un tasto viene premuto."""
    try:
        print(f"Tasto premuto: {key.char}")
    except AttributeError:
        print(f"Tasto speciale premuto: {key}")

def on_release(key):
    """Funzione chiamata quando un tasto viene rilasciato."""
    print(f"Tasto rilasciato: {key}")
    # Ferma l'ascolto quando si preme Esc
    if key == keyboard.Key.esc:
        print("Esc premuto, fermo l'ascolto.")
        return False

def main():
    print("Avvio ascolto della tastiera. Premi 'Esc' per uscire.")
    # Crea un listener per gli eventi di pressione e rilascio dei tasti
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # Attende che il listener termini

if __name__ == "__main__":
    main()
