from xmlrpc.server import SimpleXMLRPCServer

def solicitar_recurso(self, client_id):
    if not self.flag:
        self.flag = True
        self.client_id = client_id
        return True
    else:
        return False

def liberar_recurso(self, client_id):
    if self.flag and self.client_id == client_id:
        self.flag = False
        self.client_id = None
        return True
    else:
        return False

server = SimpleXMLRPCServer(("192.168.0.115", 8000))


self.flag = False  # Indica se o recurso está em uso
self.client_id = None  # ID do cliente que possui o recurso

server.serve_forever()
