# Cliente (client.py)
import xmlrpc.client
import time
proxy = xmlrpc.client.ServerProxy("http://192.168.0.115:8000/")


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
# Simulação de eventos
while(0 == 0)
  imput("evento")
  print("Tempo lógico após evento local:", local_time)
  remote_time = proxy.update_time(local_time)  # Envio de mensagem
  local_time = max(local_time, remote_time) + 1
  print("Tempo lógico após envio de mensagem:", local_time)
