from xmlrpc.server import SimpleXMLRPCServer
import time

def update_time(remote_time):
  """
  Atualiza o `local_time` com o valor máximo entre o `remote_time` e o `local_time` atual, 
  adicionando 1.
  """
  global local_time
  local_time = max(local_time, remote_time) + 1
  return local_time

local_time = 0 # Inicialização do tempo lógico local

server = SimpleXMLRPCServer(("192.168.0.115", 8000))
server.register_function(update_time, "update_time")

def increment_local_time():
  """
  Incrementa o `local_time` a cada segundo.
  """
  global local_time
  local_time += 1

# Inicia um timer para incrementar o `local_time` a cada segundo
timer = time.time()
while True:
  # Verifica se o timer já passou de um segundo
  if time.time() - timer > 1:
    increment_local_time()
    timer = time.time()

  # Processa as requisições RPC
  server.handle_request()
