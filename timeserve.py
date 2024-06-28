from xmlrpc.server import SimpleXMLRPCServer
import threading
import time

# Função que atualiza o tempo lógico
def update_time(remote_time):
    global local_time
    local_time = max(local_time, remote_time) + 1
    return local_time

# Função que incrementa o tempo lógico periodicamente
def increment_local_time():
    global local_time
    while True:
        time.sleep(1)  # Espera 1 segundo
        local_time += 1

local_time = 0  # Inicialização do tempo lógico local

# Cria e inicia a thread que incrementa o tempo lógico
increment_thread = threading.Thread(target=increment_local_time)
increment_thread.daemon = True
increment_thread.start()

# Criação do servidor XML-RPC
server = SimpleXMLRPCServer(("192.168.0.115", 8000))
server.register_function(update_time, "update_time")
print("Servidor rodando...")
server.serve_forever()
