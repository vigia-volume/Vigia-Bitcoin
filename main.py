import time
import json
import websocket
import ssl

# ==============================================================================
# TRADUÇÃO OFICIAL: O VIGIA - V2.2 (PROTOCOL_TLSv1_2 FORÇADO)
# ==============================================================================

ATIVO = "Bitcoin"
PLATAFORMA = "Tourex"
TOKEN_SSID = "Af0F2Uwn43evjshet" 

ROTAS_SERVIDORES = [
    "wss://api-prod.po.capital/socket.io/?EIO=3&transport=websocket",
    "wss://api-eu.po.market/socket.io/?EIO=3&transport=websocket"
]
rota_atual_index = 0

print("[SISTEMA] Motor de Exaustão inicializado...")
print(f"[SISTEMA] Forçando Criptografia TLSv1.2 para Windows Antigo...")

def on_message(ws, message):
    if message == "3":
        ws.send("2")
        return
    if "ping" in message: 
        ws.send('42["p"]')
    else: 
        print(f"[DADOS RECEBIDOS] {message[:120]}")

def on_error(ws, error):
    pass

def on_close(ws, close_status_code, close_msg):
    global rota_atual_index
    rota_atual_index = (rota_atual_index + 1) % len(ROTAS_SERVIDORES)
    time.sleep(3)
    conectar_plataforma()

def on_open(ws):
    print("[CONEXÃO] Canal estabelecido! Autenticando sessão...")
    payload_auth = {"ssid": TOKEN_SSID, "user_id": 0, "platform": 1}
    ws.send(f'42["auth",{json.dumps(payload_auth)}]')
    
    time.sleep(1)
    print(f"[ALVO] Solicitando streaming para o nome exato: {ATIVO}")
    payload_stream = {"asset": ATIVO, "period": 60}
    ws.send(f'42["changeSymbol",{json.dumps(payload_stream)}]')

def conectar_plataforma():
    url_alvo = ROTAS_SERVIDORES[rota_atual_index]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://pocketoption.com"
    }
    ws = websocket.WebSocketApp(
        url_alvo,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=headers
    )
    
    # Criamos um contexto SSL forçando o TLS v1.2, que o Windows 7 modificado suporta com estabilidade
    contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    contexto_ssl.check_hostname = False
    contexto_ssl.verify_mode = ssl.CERT_NONE
    
    ws.run_forever(sslopt={"context": contexto_ssl})

if __name__ == "__main__":
    conectar_plataforma()

