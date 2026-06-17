import os
import time
import threading
import pandas as pd
import pandas_ta as ta
from iqoptionapi.stable_api import IQ_Option
from flask import Flask

# Configurações do Comandante
PAUSA = 5
RSI_PERIODO = 14
ATIVO = "BTCUSD"
TIMEFRAME = 900
VALORES_OPERACAO = [1.00, 1.70, 3.50, 8.50, 20.00, 50.00, 110.00]

# Conexão e Autenticação
api = IQ_Option(os.environ.get("EMAIL_IQ"), os.environ.get("SENHA_IQ"))
if api.connect():
    print("Conectado com sucesso!")
    api.change_balance("PRACTICE")  # Forçando conta Demo
else:
    print("Erro ao conectar.")

u_b = 0
nivel_operacao = 0
candles_historico = []

def calcular_vigia(df):
    df['rsi'] = ta.rsi(df['close'], length=RSI_PERIODO)
    df['tem_respiro_alta'] = (df['close'].shift(2) < df['open'].shift(2)) & (df['close'].shift(3) < df['open'].shift(3))
    df['tem_respiro_baixa'] = (df['close'].shift(2) > df['open'].shift(2)) & (df['close'].shift(3) > df['open'].shift(3))
    df['f_alta_ante'] = (df['close'] > df['open']) & (df['close'].shift(1) < df['open'].shift(1))
    df['f_baixa_ante'] = (df['close'] < df['open']) & (df['close'].shift(1) > df['open'].shift(1))
    
    s_f_azul = df['f_alta_ante'] & (len(df) - u_b > PAUSA) & (df['rsi'] < 60) & df['tem_respiro_alta']
    s_f_laranja = df['f_baixa_ante'] & (len(df) - u_b > PAUSA) & (df['rsi'] > 40) & df['tem_respiro_baixa']
    return s_f_azul, s_f_laranja

def executar_operacao(direcao):
    global nivel_operacao
    valor = VALORES_OPERACAO[nivel_operacao]
    print(f"Executando {direcao} com {valor} USD (Nível {nivel_operacao + 1})")
    
    # Aqui o robô executa a entrada na Tourex
    # O valor é pego da lista VALORES_OPERACAO conforme o nível de prejuízo
    
    nivel_operacao = (nivel_operacao + 1) % len(VALORES_OPERACAO)

def rotina_principal():
    global u_b
    while True:
        c = api.get_candles(ATIVO, TIMEFRAME, 1, time.time())
        if c:
            candles_historico.append({'open': c[0]['open'], 'close': c[0]['close']})
            if len(candles_historico) > 20:
                df = pd.DataFrame(candles_historico)
                s_azul, s_laranja = calcular_vigia(df)
                if s_azul.iloc[-1]:
                    executar_operacao("Compra")
                    u_b = len(df)
                elif s_laranja.iloc[-1]:
                    executar_operacao("Venda")
                    u_b = len(df)
        time.sleep(60)

app = Flask(__name__)
@app.route('/')
def home(): return "Sistema Operando na Conta Demo!"

if __name__ == "__main__":
    threading.Thread(target=rotina_principal, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

