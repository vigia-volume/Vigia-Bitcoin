import pandas as pd
import pandas_ta as ta

# CONFIGURAÇÕES DO COMANDANTE
PAUSA = 5
RSI_PERIODO = 14
VOLUME_ALVO = 2.0

# Variáveis de Estado
u_b = 0  # Ultima barra de operação
candles = []

def calcular_vigia(df):
    # Tradução do Pine Script
    df['rsi'] = ta.rsi(df['close'], length=RSI_PERIODO)
    
    # Lógica de Respiro (2 velas contrárias)
    df['tem_respiro_alta'] = (df['close'].shift(2) < df['open'].shift(2)) & (df['close'].shift(3) < df['open'].shift(3))
    df['tem_respiro_baixa'] = (df['close'].shift(2) > df['open'].shift(2)) & (df['close'].shift(3) > df['open'].shift(3))
    
    # Lógica de Antecipação (2ª vela)
    df['f_alta_ante'] = (df['close'] > df['open']) & (df['close'].shift(1) < df['open'].shift(1))
    df['f_baixa_ante'] = (df['close'] < df['open']) & (df['close'].shift(1) > df['open'].shift(1))
    
    # Sinais
    s_f_azul = df['f_alta_ante'] & (len(df) - u_b > PAUSA) & (df['rsi'] < 60) & df['tem_respiro_alta']
    s_f_laranja = df['f_baixa_ante'] & (len(df) - u_b > PAUSA) & (df['rsi'] > 40) & df['tem_respiro_baixa']
    
    return s_f_azul, s_f_laranja

# O loop principal processará os dados da Tourex aqui
def processar_fluxo(novo_candle):
    global u_b
    candles.append(novo_candle)
    if len(candles) > 20:
        df = pd.DataFrame(candles)
        s_azul, s_laranja = calcular_vigia(df)
        
        if s_azul.iloc[-1]:
            print("SINAL: Fluxo Azul - Entrada de Compra")
            u_b = len(df)
        elif s_laranja.iloc[-1]:
            print("SINAL: Fluxo Laranja - Entrada de Venda")
            u_b = len(df)

