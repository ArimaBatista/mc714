from xmlrpc.client import ServerProxy
import uuid

client_id = str(uuid.uuid1())

def solicitar_recurso(serve):
        # Tenta pegar o recurso
        resultado = server.solicitar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} obteve o recurso.")
        else:
            print(f"Cliente {client_id} não obteve o recurso. Recurso em uso.")
        return resultado

def liberar_recurso(self):
        # Tenta liberar o recurso
        resultado = server.liberar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} liberou o recurso.")
        else:
            print(f"Cliente {client_id} não pôde liberar o recurso. Possível erro.")


end_serve = "http://192.168.0.115:8000"

server = ServerProxy(end_serve)

while True:
    input("Pegar Recurso")
    solicitar_recurso(serve)
    input("Liberar Recurso")
    liberar_recurso(serve)
