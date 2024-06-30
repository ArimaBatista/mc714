from xmlrpc.server import SimpleXMLRPCServer

flag = False  # Indica se o recurso está em uso
client = None  # ID do cliente que possui o recurso

def solicitar_recurso(client_id):
    global flag
    global client
    if not flag:
        flag = True
        client = client_id
        return True
    else:
        return False

def liberar_recurso(client_id):
    global flag
    global client
    if flag and client == client_id:
        flag = False
        client = None
        return True
    else:
        return False

server = SimpleXMLRPCServer(("192.168.0.115", 8000))
print("Servidor XML-RPC em execução...")

server.register_function(solicitar_recurso, "solicitar_recurso")
server.register_function(liberar_recurso, "liberar_recurso")

server.serve_forever()
