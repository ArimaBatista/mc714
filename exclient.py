from xmlrpc.client import ServerProxy

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
        # Implemente a lógica para gerar um ID único para o cliente
        # (pode ser um UUID, um número sequencial, etc.)
        return "meu_id_unico"  # Substitua por sua lógica de geração de ID

# Exemplo de uso
cliente = ExclusaoMutuaCliente("http://192.168.0.115:8000")
while (0==0):
    t = input("Pegar Recurso")
    cliente.solicitar_recurso()
    t = input("Liberar Recurso")
    cliente.liberar_recurso()
