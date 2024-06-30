from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import re

endereco_ip = "192.168.0.118"

# Lista de clientes e líder
client = []
lider = None

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
    lider = endereco_ip
    for x in lista:
        y = re.sub(r'[^0-9]', '', x)
        y = int(y)
        if y > id:
            try:
                p = f"http://{x}:8000"
                serve = ServerProxy(p)
                verifica = serve.ativo()
                if verifica == "ativo":
                    lider = x
            except:
                client.remove(x)
    return lider

# Criar o servidor XML-RPC
server = SimpleXMLRPCServer((endereco_ip, 8000))
print(f"Servidor em execução no endereço {endereco_ip}:8000")

# Registrar funções no servidor
server.register_function(ativo, "ativo")
server.register_function(registro, "registro")
server.register_function(obter_lider, "obter_lider")
server.register_function(eleicao, "eleicao")

# Iniciar o servidor
server.serve_forever()
