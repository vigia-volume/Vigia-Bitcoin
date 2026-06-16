import os
import threading
from flask import Flask
from iqoptionapi.stable_api import IQ_Option

# Busca direto das variáveis de ambiente configuradas no Render
email = os.environ.get("EMAIL_IQ")
senha = os.environ.get("SENHA_IQ")

api = IQ_Option(email, senha)
api.connect()

app = Flask(__name__)

@app.route('/')
def home():
    if api.check_connect():
        return "Conectado à IQ Option com sucesso, Comandante!"
    else:
        return "Falha na conexão. Verifique as Environment Variables."

def rotina_principal():
    print("Monitoramento iniciado...")
    # Aqui inseriremos a lógica de exaustão em breve
    while True:
        pass

if __name__ == "__main__":
    threading.Thread(target=rotina_principal).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

