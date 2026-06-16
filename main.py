from iqoptionapi.stable_api import IQ_Option
from flask import Flask
import threading
import os

# Função para ler credenciais do Secret File
def ler_credenciais():
    try:
        with open("/etc/secrets/credenciais", "r") as f:
            d = {l.split('=')[0].strip(): l.split('=')[1].strip() for l in f.read().splitlines()}
        return d['EMAIL_IQ'], d['SENHA_IQ']
    except Exception as e:
        print(f"Erro ao ler credenciais: {e}")
        return None, None

email, senha = ler_credenciais()
api = IQ_Option(email, senha)
api.connect()

app = Flask(__name__)

@app.route('/')
def home():
    if api.check_connect():
        return "Conectado à IQ Option com sucesso!"
    else:
        return "Falha na conexão."

def rotina_principal():
    print("Monitoramento iniciado...")
    # Aqui colocaremos a lógica de exaustão em breve
    while True:
        pass

if __name__ == "__main__":
    threading.Thread(target=rotina_principal).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

