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
'''
import xmlrpc.client                                          #para usar os comandos referentes ao cliente
proxy = xmlrpc.client.ServerProxy("endereço ip + porta")      #para criar o proxy para o servidor (mais ou menos oque vai fala pro cliente o caminho pro servidor) devesse colocar o endereço ip mais a porta a ser usada
proxy.Nome_da_função()                                        #liga o cliente a função declarada no servidor

'''
from xmlrpc.server import SimpleXMLRPCServer     #para usar os comandos referentes ao Server



'''
