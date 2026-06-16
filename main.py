import time

def main():
    print("Iniciando teste de comunicação...")
    while True:
        print("Comunicação estável: O sistema está vivo.")
        time.sleep(60) # Espera 60 segundos antes de repetir

if __name__ == "__main__":
    main()

