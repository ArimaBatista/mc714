from xmlrpc.client import ServerProxy
import uuid

client_id = uuid.uuid1()

class ExclusaoMutuaCliente:
    def __init__(self, server_address):
        self.server = ServerProxy(server_address)

    def solicitar_recurso(self):
        #tenta pega o rec
        resultado = self.server.solicitar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} obteve o recurso.")
        else:
            print(f"Cliente {client_id} não obteve o recurso. Recurso em uso.")
        return resultado

    def liberar_recurso(self):
        #tenta libera o rec
        resultado = self.server.liberar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} liberou o recurso.")
        else:
            print(f"Cliente {client_id} não pôde liberar o recurso. Possível erro.")




cliente = ExclusaoMutuaCliente("http://192.168.0.115:8000")
while (0==0):
    t = input("Pegar Recurso")
    cliente.solicitar_recurso()
    t = input("Liberar Recurso")
    cliente.liberar_recurso()
