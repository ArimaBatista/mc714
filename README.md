# Relatorio do trabalho
## Objetivos do trabalho
Elaborar 3 algoritimos que demonstram conhecimento em Sistemas Distribuidos sendo eles:
- Relógio lógico de Lamport.
- Algoritmo de exclusão mútua.
- Algoritmo de eleição de líder

Logo teria que implementar um meio de comunicação entre os sistemas, e para esse problema vou usar RPC que falaremos masi a diante.

## Preparação 
Para Simular esses algoritimos vamos precisar de mais de um sistema ligados na mesma rede então vamos usar o [virtualbox](https://www.virtualbox.org/) e usaremos [ubunto](https://ubuntu.com/download)
e apos criado pelo menos 3 maquinas virtuais precisamos configa a interface de rede em  __modo bridge__ 
![image](https://github.com/ArimaBatista/mc714/assets/80778627/13061a02-d53c-42d6-8a62-a799ce49da11)

após feito isso as maquinas estarão na mesma rede e vamos intalar os pacotes necessarios __python3__ e __rpcblind__ 

## O algoritmo
### Comunicação RPC
Para elaborara comunicação RPC vamos usar a biblioteca [xmlrpc](https://docs.python.org/pt-br/3/library/xmlrpc.html)
No [cliente](https://docs.python.org/pt-br/3/library/xmlrpc.client.html#module-xmlrpc.client) usaremos:
```
import xmlrpc.client                                          #para usar os comandos referentes ao cliente
proxy = xmlrpc.client.ServerProxy("endereço ip + porta")      #para criar o proxy para o servidor (mais ou menos oque vai fala pro cliente o caminho pro servidor) devesse colocar o endereço ip mais a porta a ser usada
proxy.Nome_da_função()                                        #liga o cliente a função declarada no servidor
```
No [servidor](https://docs.python.org/pt-br/3/library/xmlrpc.server.html#module-xmlrpc.server):
```
from xmlrpc.server import SimpleXMLRPCServer               #para usar os comandos referentes ao Server
server = SimpleXMLRPCServer(("192.168.0.115", 8000))       #Configura o endereço do servidor e porta
server.Nome_da_função(Variavel, "Variavel")                #Para declarar as funçãos que podem ser acessadas pelo cliente
server.serve_forever()                                     #Para "subir" o servidor
```
Essa estrutura basica vai se repitir ao longo dos 3 algoritimos 
### Relogio Lamporte
Nesses algoritmos cada processo do sistema distribuído mantém um contador crescente e monotônico C (relógio lógico) e cada evento a possui uma marca temporal C(a) na qual todos os processos concordam. Dessa forma, os eventos estão sujeitos às seguintes propriedades derivadas da relação happens-before:
* Se a acontece antes de b no mesmo processo, então C(a) < C(b).
* Se a e b representam, respectivamente, o envio e o recebimento de uma mensagem, então C(a) < C(b).
* Sejam a e b eventos quaisquer, então C(a) ≠ C(b)
[wikikpedia](https://pt.wikipedia.org/wiki/Rel%C3%B3gios_de_Lamport)
![image](https://github.com/ArimaBatista/mc714/assets/80778627/d37d8d84-bfc6-4b69-b8d4-061680ce0b65)
  [link](https://angelicaribeirodotcom.wordpress.com/2017/09/02/sistemas-distribuidos/)

Alem da entrutura basica vamos precisar implementar um relogio local tanto no servidor quanto no cliente
```
import time
import threading
def increment_local_time():
    global local_time
    while True:
        time.sleep(1)  # Espera 1 segundo
        local_time += 10

local_time = 0  # Inicialização do tempo lógico local

# Cria e inicia a thread que incrementa o tempo lógico
increment_thread = threading.Thread(target=increment_local_time)
increment_thread.daemon = True
increment_thread.start()
```
onde o [time](https://docs.python.org/3/library/time.html) fica responsael para contar o tempo e o [thearding](https://docs.python.org/3/library/threading.html) para que o relogio funcione em segundo plano
sabendo disso bastaimplementar que envia seu relogio e que recebe e compara com seu relogio e incorpora o maior e o incrementa como
```
#no server
# Função que atualiza o tempo lógico
def update_time(remote_time):
    global local_time
    local_time = max(local_time, remote_time) + 1
    return local_time
#no cliente
remote_time = proxy.update_time(local_time)  # Envio de mensagem
local_time = max(local_time, remote_time) + 1
```
juntando isso a estrutura ja mencionada teremos noisso codigo.
parra ver os codigos completos pode clicar em [Cliente](https://github.com/ArimaBatista/mc714/blob/main/timeclient.py) e/ou [Servidor](https://github.com/ArimaBatista/mc714/blob/main/timeserve.py)
