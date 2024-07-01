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

### Agoritmo de Exclusão Multua
Exclusão mútua (também conhecida pelo acrônimo mutex para mutual exclusion, o termo em inglês) é uma técnica usada em programação concorrente para evitar que dois processos ou threads tenham acesso simultaneamente a um recurso compartilhado, acesso esse denominado por seção crítica.[wikipedia](https://pt.wikipedia.org/wiki/Exclus%C3%A3o_m%C3%BAtua)
Para implementar esse algortmo podemos criar uma flag que representa a "chave" para pegar o recurso sinalia que pegou e da seu endereço de ip para saber quem tem direto de devolver a "chave" e alterar o recurso e apartir que ele pega a chave ele bloqueia outros de pegarem a chave
no Servidor:
[link para codigo completo](https://github.com/ArimaBatista/mc714/blob/main/exclusaoserver.py)
```
flag = False  # Indica se o recurso está em uso
client = None  # ID do cliente que possui o recurso

def solicitar_recurso(client_id):
    global flag
    global client
    if not flag:
        flag = True
        client = client_id
        return True
    else:
        return False

def liberar_recurso(client_id):
    global flag
    global client
    if flag and client == client_id:
        flag = False
        client = None
        return True
    else:
        return False
```
no cliente:
[Link para o codigo Completo](https://github.com/ArimaBatista/mc714/blob/main/exclusaoclient.py)
```
import uuid #para gerar um end de ip

client_id = str(uuid.uuid1())

end_serve = "http://192.168.0.115:8000"

serve = ServerProxy(end_serve)

def solicitar_recurso():
        # Tenta pegar o recurso
        resultado = serve.solicitar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} obteve o recurso.")
        else:
            print(f"Cliente {client_id} não obteve o recurso. Recurso em uso.")
        return resultado

def liberar_recurso():
        # Tenta liberar o recurso
        resultado = serve.liberar_recurso(client_id)
        if resultado:
            print(f"Cliente {client_id} liberou o recurso.")
        else:
            print(f"Cliente {client_id} não pôde liberar o recurso. Possível erro.")

```

### Algoritimo de Eleição de Lider
Eleição de líder é um problema da área de sistemas distribuídos que busca selecionar de forma consensual um processo num conjunto de processos tendo como objetivo selecionar um líder para uma determinada tarefa. A eleição torna-se necessária quando o sistema distribuído está sendo iniciado pela primeira vez ou o líder anterior não consegue se comunicar com os demais processos pela ocorrência de alguma falha. Há vários algoritmos que realizam a eleição do líder, cada um específico a alguma situação.[wikipedia](https://pt.wikipedia.org/wiki/Elei%C3%A7%C3%A3o_de_l%C3%ADder#:~:text=Algoritmo%20em%20anel&text=A%20execu%C3%A7%C3%A3o%20do%20algoritmo%20busca,n%C3%B3%20ao%20vizinho%20da%20direita.)

Esse algoritmo é o masi complexo porque exige a troca de informação attiva ente todos os nós da rede, vamos começar pensando nisso logo no cliente[link para o codigo completo](https://github.com/ArimaBatista/mc714/blob/main/liderclient.py) vamos implementar uma funcão que verifica quais nos estão ativos e quais não estão para facilitar a nossa vida ele ja vai aproveitar e pergunta quem é o lider para que o usuario tenha confirmação visual que é o mesmo lider em todos os ativos:
```
endereco_ip =#localhost ["http://192.168.0.115:8000", "http://192.168.0.116:8000", "http://192.168.0.118:8000"]

# Lista de endereços do servidor
end_serve = ["http://192.168.0.115:8000", "http://192.168.0.116:8000", "http://192.168.0.118:8000"]

while True:
    t = input("atualiar?")
    for x in end_serve:
        try:
            serve = ServerProxy(x)
            dado = serve.obter_lider()
            print(f"Líder do servidor {x} é {dado}")
        except Exception as e:
            print(f"Servidor {x} está desativado. Erro: {e}")
```

Agora vamos  pensar em como o servidor confirma se o lider esta ativo caso ele não esteja vai ter que chamar uma eleição:

```
endereco_ip = "192.168.0.115"

# Lista de clientes e líder
client = ["http://192.168.0.115:8000", "http://192.168.0.116:8000", "http://192.168.0.118:8000"]
lider = 0

def ativo():
    return "ativo"

def obter_lider():
    global lider
    global endereco_ip
    try:
        if lider != endereco_ip:
            p = f"http://{lider}:8000"
            serve = ServerProxy(p)
            verifica = serve.ativo()
            if verifica == "ativo":
                return lider
        else:
            return lider
    except:
        eleicao()
    return lider

```
Vamos pensar como funciona a eleição que ocorre da segunte maneireira; ao detectar que o servidor lider não responde ele tenta chamar os nos que tem ip maior que o dele caso não tenha ninguem ou que nao tenha resposta ele se declara o lider caso um maior responda ele sera o lider até que chegue alguem maior, cale ressaltar que se um maior volta a responder ele toma o comando:
```
def eleicao():
    global client
    global endereco_ip
    global lider
    id = re.sub(r'[^0-9]', '', endereco_ip)
    id = int(id)
    lista = sorted(client)
    for x in lista:
        y = re.sub(r'[^0-9]', '', x)
        y = int(y) // 10000
        if id < y:
            try:
                serve = ServerProxy(x)
                verifica = serve.ativo()
                if verifica == "ativo":
                    lider = x
            except:
                print("server off")
        if y == id:
            lider = "http://"+endereco_ip+":8000"
    return lider
```
usei tambem  abiblioteca [re](https://docs.python.org/3/library/re.html) para manipular variaveis
[Link para o codigo completo](https://github.com/ArimaBatista/mc714/blob/main/liderserver.py)

## Testes Realiados:

# Relogio Lamporte

Para tal usei duas maquinas virtuas uma servindo como servidor e outra como cliente e deixei propositalmente o relogio do servidor 10x masi papido para visualiar o as atualiações do relogio do cliente 
![image](https://github.com/ArimaBatista/mc714/assets/80778627/f8316bd6-c0ea-430c-8114-7eaa105cb85d)
podemos visualiar claramente o relogio do clinte se atualiando após a troca das mensagens

# Exclusão Multua

para isso usei 2 Maquians virtuais uma servindo de cliente e servidor e outra de cliente
![image](https://github.com/ArimaBatista/mc714/assets/80778627/3d1d0d72-2189-4809-998c-c7343e96ad6d)

podemos visualiar que enquanto uma estava com recurso a outra não conseguia pegar o recurso enquanto a outra não a liberasse e que a qual não estavas com o recurso não conseguia não conseguia liberar o recurso que não ela dela.

# Algoritmo de Eleição de Lider

Para esse problema criei 3 maquiuans Virtuais todas como Servidor e Cliente para visualiar se o havia consenso entre lider quando uma estava ativa duas e tres ativas e quando havia uma falha da lider se outra tomava o lugar de lider e quando o lider voltava a ativa podemos visualiar oque aconteceu nas fostos que estarão em ordem cronologica respectivamente ativando na ordem de final de ip 115 118 e 116 respectivamente:
ligando o serve de ip final 115:
![image](https://github.com/ArimaBatista/mc714/assets/80778627/0b415134-8777-49d9-8223-f14a7faa75af)
ligando o serve de final 118:
![image](https://github.com/ArimaBatista/mc714/assets/80778627/860f8d3c-1ff3-40ed-8136-d1ecdfdcf930)
podemos ver que ja atualiou o lider

ligando o serve de final 116:
![image](https://github.com/ArimaBatista/mc714/assets/80778627/473b1058-e088-46fa-99c7-4efe703a1d69)
que não toma o lugar de lider pelo seu endereço ip

Queda do servidor lider:
![image](https://github.com/ArimaBatista/mc714/assets/80778627/9be205a0-42c1-47cd-8ca0-e5888dead28b)
onde o serve 116 toma o lugar do lider

volta do servidor 118:
![image](https://github.com/ArimaBatista/mc714/assets/80778627/201e909d-fb0e-4fbf-833f-93f3a4fe9d1a)
tomando o posto de lider



Fontes
- https://docs.python.org/pt-br/3/library/xmlrpc.client.html#module-xmlrpc.client
- https://docs.python.org/pt-br/3/library/xmlrpc.server.html#module-xmlrpc.server
- https://pt.wikipedia.org/wiki/XML-RPC
- https://pt.wikipedia.org/wiki/Rel%C3%B3gios_de_Lamport
- https://angelicaribeirodotcom.wordpress.com/2017/09/02/sistemas-distribuidos/?irclickid=xSSQvCzCXxyKReH2wizkux6LUkC0re2W9whOTA0&sharedid=234017&irpid=123201&utm_source=impact&utm_medium=affiliate&irgwc=1
- https://docs.python.org/3/library/threading.html
- https://docs.python.org/3/library/time.html
- https://docs.python.org/3/library/re.html
- https://pt.wikipedia.org/wiki/Exclus%C3%A3o_m%C3%BAtua
- https://pt.wikipedia.org/wiki/Elei%C3%A7%C3%A3o_de_l%C3%ADder#:~:text=Algoritmo%20em%20anel&text=A%20execu%C3%A7%C3%A3o%20do%20algoritmo%20busca,n%C3%B3%20ao%20vizinho%20da%20direita.
- https://chatgpt.com/

