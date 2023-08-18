import requests
import sys
from hfc.fabric import Client as client_fabric
from hfc.fabric_network.gateway import Gateway
from hfc.fabric_network.network import Network
from hfc.fabric_network.contract import Contract
import asyncio
from datetime import datetime
import time
import json

domain = ["connection-org1"]
channel_name = "mychannel"
cc_name = "fieldclimate"
cc_version = "1.0"

# leitura do arquivo
stationID = '0120C6A2'
with open(f'blockchain/gateway/fieldclimate/json/{stationID}_output.json', 'r') as file:
    jsonFile = json.load(file)    

# pegando o horário mais atual
lastUpdated = jsonFile['dates'][6]

# navegando para a área de dados (data)
data = jsonFile['data']

# função de escanear dados específicos
def jsonScan(json_object, name):
    deviceName = name
    deviceType = [obj for obj in json_object if obj['name']==name][0]['type']
    unit = [obj for obj in json_object if obj['name']==name][0]['unit']
    values = [obj for obj in json_object if obj['name']==name][0]['values']

    return deviceName, deviceType, unit, values

deviceName, deviceType, unit, values = jsonScan(data, 'Solar Panel')

# Convertendo data para unix timestamp
lastUpdate = lastUpdated.replace('-', '/')
formato = "%Y/%m/%d %H:%M:%S"
aux = datetime.strptime(lastUpdate, formato)
lastUpdateUnix = aux.timestamp()
print(f'Horário de inserção dos dados: {lastUpdate}')
print(f'Horário de inserção dos dados em Unix: {lastUpdateUnix}')

if __name__ == "__main__":

    #test if the city name was informed as argument
    if len(sys.argv) != 1: # o primeiro  argumento sempre vai ser o chamado do python
        print("Usage:",sys.argv[0])
        exit(1)

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
    
    response = loop.run_until_complete(c_hlf.chaincode_invoke(
            requestor=admin,
            channel_name=channel_name,
            peers=['peer0.org1.example.com', 'peer0.org2.example.com'],
            args=[stationID, deviceName, deviceType, unit, values, lastUpdateUnix, clientExecutionUnix],
            fcn= 'InsertStationData',
            cc_name=cc_name,
            wait_for_event=True,  # optional, for private data
            # for being sure chaincode invocation has been commited in the ledger, default is on tx event
            #cc_pattern="^invoked*"  # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
            ))
    print(response)
    print('Dados inseridos com sucesso!')


    response = loop.run_until_complete(c_hlf.chaincode_invoke(
        requestor=admin,
        channel_name=channel_name,
        peers=['peer0.org1.example.com', 'peer0.org2.example.com'],
        args=[stationID, deviceName],
        fcn= 'ReadStationData',
        cc_name=cc_name,
        wait_for_event=True,  # optional, for private data
        # for being sure chaincode invocation has been commited in the ledger, default is on tx event
        #cc_pattern="^invoked*"  # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
        ))
    print(response)

