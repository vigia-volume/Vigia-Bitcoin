import threading
import http.server
import socketserver
import os

# Função para manter o Render feliz (servidor HTTP básico)
def run_web_server():
    PORT = int(os.environ.get("PORT", 10000))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

# Inicia o servidor web em segundo plano
server_thread = threading.Thread(target=run_web_server)
server_thread.daemon = True
server_thread.start()

# --- SUA LÓGICA PRINCIPAL COMEÇA AQUI ---
print("Sistema de monitoramento iniciado...")
# Coloque aqui o seu código de análise da Tourex
while True:
    pass 
# ----------------------------------------

