from xmlrpc.client import ServerProxy

endereco_ip = ["http://192.168.0.115:8000", "http://192.168.0.116:8000", "http://192.168.0.118:8000"]

# Lista de endereços do servidor
end_serve = ["http://192.168.0.115:8000", "http://192.168.0.116:8000", "http://192.168.0.118:8000"]

while True:
    t = input("atualiar?")
    for x in end_serve:
        try:
            serve = ServerProxy(x)
            serve.registro(endereco_ip)
            dado = serve.lider()
            print(f"Líder do servidor {x} é {dado}")
        except Exception as e:
            print(f"Servidor {x} está desativado. Erro: {e}")
