import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Online"

def rotina_principal():
    # AQUI ENTRA O SEU CÓDIGO ORIGINAL DA TOUREX
    print("Monitoramento ativo...")

if __name__ == "__main__":
    threading.Thread(target=rotina_principal).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

