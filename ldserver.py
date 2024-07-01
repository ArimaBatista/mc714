from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import re

endereco_ip = "192.168.0.115"

# Lista de clientes e líder
client = ["http://192.168.0.115:8000", "http://192.168.0.116:8000", "http://192.168.0.118:8000"]
lider = 0

def ativo():
    return "ativo"

def registro(client_id):
    global client
    if client_id not in client:
        client.append(client_id)
        eleicao()
        return "usuario registrado"
    else:
        return "usuario ja registrado"

def obter_lider():
    global lider
    global endereco_ip
    try:
        if lider != endereco_ip:
            p = f"http://{lider}:8000"
            serve = ServerProxy(p)
            verifica = serve.ativo()
            if verifica == "ativo":
                return lider
        else:
            return lider
    except:
        eleicao()
    return lider

def eleicao():
    global client
    global endereco_ip
    global lider
    id = re.sub(r'[^0-9]', '', endereco_ip)
    id = int(id)
    lista = sorted(client)
    for x in lista:
        y = re.sub(r'[^0-9]', '', x)
        y = int(y) // 10000
        if id < y:
            print("tttt")
            try:
                print("retsert")
                serve = ServerProxy(x)
                verifica = serve.ativo()
                print("sr")
                if verifica == "ativo":
                    lider = x
            except:
                print("server off")
        if y == id:
            lider = "http://"+endereco_ip+":8000"
    return lider

# Criar o servidor XML-RPC
server = SimpleXMLRPCServer((endereco_ip, 8000))
print(f"Servidor em execução no endereço {endereco_ip}")

# Registrar funções no servidor
server.register_function(ativo, "ativo")
server.register_function(registro, "registro")
server.register_function(obter_lider, "obter_lider")
server.register_function(eleicao, "eleicao")

# Iniciar o servidor
server.serve_forever()
