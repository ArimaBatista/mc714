from xmlrpc.server import SimpleXMLRPCServer

flag = False  # Indica se o recurso está em uso
client = None  # ID do cliente que possui o recurso

def solicitar_recurso(client_id):
    if not flag:
        flag = True
        client = client_id
        return True
    else:
        return False

def liberar_recurso(client_id):
    if flag and client == client_id:
        flag = False
        client_id = None
        return True
    else:
        return False

server = SimpleXMLRPCServer(("192.168.0.115", 8000))

server.serve_forever()
