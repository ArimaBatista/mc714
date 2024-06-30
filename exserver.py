from xmlrpc.server import SimpleXMLRPCServer

class ExclusaoMutuaServer:
    def __init__(self):
        self.flag = False  # Indica se o recurso está em uso
        self.client_id = None  # ID do cliente que possui o recurso

    def solicitar_recurso(self, client_id):
        """
        Método para solicitar acesso ao recurso.
        Retorna True se o recurso estiver disponível, False caso contrário.
        """
        if not self.flag:
            self.flag = True
            self.client_id = client_id
            return True
        else:
            return False

    def liberar_recurso(self, client_id):
        """
        Método para liberar o recurso.
        Retorna True se o cliente possuía o recurso e o liberou com sucesso, False caso contrário.
        """
        if self.flag and self.client_id == client_id:
            self.flag = False
            self.client_id = None
            return True
        else:
            return False

server = SimpleXMLRPCServer(("192.168.0.115", 8000))
server.register_instance(ExclusaoMutuaServer())
print("Servidor de Exclusão Mútua em execução na porta 8000")
server.serve_forever()
