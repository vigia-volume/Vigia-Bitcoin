from iqoptionapi.stable_api import IQ_Option
import os

def ler_credenciais():
    with open("/etc/secrets/credenciais", "r") as f:
        d = {l.split('=')[0]: l.split('=')[1].strip() for l in f.read().splitlines()}
    return d['EMAIL_IQ'], d['SENHA_IQ']

email, senha = ler_credenciais()
api = IQ_Option(email, senha)
api.connect()

if api.check_connect():
    print("Conectado com sucesso!")
else:
    print("Falha na conexão.")

