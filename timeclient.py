# Cliente (client.py)
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://192.168.0.115:8000/")
local_time = 0

# Simulação de eventos
local_time = proxy.update_time(local_time)  # Evento local
print("Tempo lógico após evento local:", local_time)
local_time = proxy.update_time(local_time)  # Envio de mensagem
print("Tempo lógico após envio de mensagem:", local_time)
