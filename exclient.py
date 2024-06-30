from xmlrpc.client import ServerProxy
import uuid

class ExclusaoMutuaCliente:
    def __init__(self, server_address):
        self.server = ServerProxy(server_address)

    def solicitar_recurso(self):
        """
        Solicita o recurso ao servidor e espera pela resposta.
        Retorna True se o recurso foi obtido com sucesso, False caso contrário.
        """
        client_id = self.get_client_id()
        resultado = self.server.solicitar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} obteve o recurso.")
        else:
            print(f"Cliente {client_id} não obteve o recurso. Recurso em uso.")
        return resultado

    def liberar_recurso(self):
        """
        Libera o recurso no servidor.
        """
        client_id = self.get_client_id()
        resultado = self.server.liberar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} liberou o recurso.")
        else:
            print(f"Cliente {client_id} não pôde liberar o recurso. Possível erro.")

    def get_client_id(self):
        # Gera um UUID baseado no endereço MAC da máquina
        unique_id = uuid.uuid1()
        return str(unique_id)

# Exemplo de uso
cliente = ExclusaoMutuaCliente("http://192.168.0.115:8000")
while (0==0):
    t = input("Pegar Recurso")
    saida = cliente.solicitar_recurso()
    if saida:
        t = input("Liberar Recurso")
        cliente.liberar_recurso()
