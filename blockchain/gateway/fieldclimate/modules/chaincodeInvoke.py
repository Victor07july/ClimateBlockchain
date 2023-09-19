import sys
from hfc.fabric import Client as client_fabric
from hfc.fabric_network.gateway import Gateway
from hfc.fabric_network.network import Network
from hfc.fabric_network.contract import Contract
import asyncio
import time

domain = ["connection-org1"]
channel_name = "mychannel"
cc_name = "fieldclimate"
cc_version = "1.0"


# ------ PEGANDO O HORÁRIO DE EXECUÇÃO DO CLIENTE --------
# Horário de execução do cliente em unix
clientExecutionUnix = time.time()
print(f'Horário de execução do cliente em UNIX: {clientExecutionUnix}')

print("Iniciando o chaincode...")
loop = asyncio.get_event_loop()
#creates a loop object to manage async transactions

new_gateway = Gateway() # Creates a new gateway instance

c_hlf = client_fabric('/home/stephanie/Inmetrochain-Vehicle/blockchain/gateway/connection-org1.json')
user = c_hlf.get_user('org1.example.com', 'User1')
admin = c_hlf.get_user('org1.example.com', 'Admin')
# print(admin)
peers = []
peer = c_hlf.get_peer('/home/stephanie/Inmetrochain-Vehicle/blockchain/gateway/connection-org1.json')
peers.append(peer)
options = {'wallet': ''}

c_hlf.new_channel(channel_name)

# função de invocar o chaincode
def invoke(chaincodeName, *argv, insertTimestamp = False):

    # declarando array
    args = []

    # loop para pegar os parametros inseridos na função
    for arg in argv:
        args.append(arg)

    print(f'Inicializando chaincode {chaincodeName}')


    # inserir tempo de execução unix caso insertTimeStamp = True
    args.append(str(clientExecutionUnix)) if insertTimestamp == True else print('Timestamp não inserido')

    response = loop.run_until_complete(c_hlf.chaincode_invoke(
        requestor=admin,
        channel_name=channel_name,
        peers=['peer0.org1.example.com', 'peer0.org2.example.com'],
        args=args,
        fcn= chaincodeName,
        cc_name=cc_name,
        wait_for_event=True,  # optional, for private data
        # for being sure chaincode invocation has been commited in the ledger, default is on tx event
        #cc_pattern="^invoked*"  # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
        ))
    print(f'Resposta: {response}')
    print(f'Execução do chaincode {chaincodeName} finalizada')

    return response