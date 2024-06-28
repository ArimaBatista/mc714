from xmlrpc.server import SimpleXMLRPCServer

def update_time(remote_time):
    global local_time
    local_time = max(local_time, remote_time) + 1
    return local_time

local_time = 0  # Inicialização do tempo lógico local

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(update_time, "update_time")
server.serve_forever()
