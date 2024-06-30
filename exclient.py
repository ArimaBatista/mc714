from xmlrpc.client import ServerProxy
import uuid

client_id = str(uuid.uuid1())

class ExclusaoMutuaCliente:
    def __init__(self, server_address):
        self.server = ServerProxy(server_address)

    def solicitar_recurso(self):
        # Tenta pegar o recurso
        resultado = self.server.solicitar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} obteve o recurso.")
        else:
            print(f"Cliente {client_id} não obteve o recurso. Recurso em uso.")
        return resultado

    def liberar_recurso(self):
        # Tenta liberar o recurso
        resultado = self.server.liberar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} liberou o recurso.")
        else:
            print(f"Cliente {client_id} não pôde liberar o recurso. Possível erro.")

cliente = ExclusaoMutuaCliente("http://192.168.0.115:8000")
while True:
    input("Pegar Recurso")
    cliente.solicitar_recurso()
    input("Liberar Recurso")
    cliente.liberar_recurso()
