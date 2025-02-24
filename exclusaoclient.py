from xmlrpc.client import ServerProxy
import uuid

client_id = str(uuid.uuid1())

end_serve = "http://192.168.0.115:8000"

serve = ServerProxy(end_serve)

def solicitar_recurso():
        # Tenta pegar o recurso
        resultado = serve.solicitar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} obteve o recurso.")
        else:
            print(f"Cliente {client_id} não obteve o recurso. Recurso em uso.")
        return resultado

def liberar_recurso():
        # Tenta liberar o recurso
        resultado = serve.liberar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} liberou o recurso.")
        else:
            print(f"Cliente {client_id} não pôde liberar o recurso. Possível erro.")



while True:
    input("Pegar Recurso")
    solicitar_recurso()
    input("Liberar Recurso")
    liberar_recurso()
