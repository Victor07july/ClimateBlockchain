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

with open('json/general_output.json', 'r') as file:
    data = json.load(file)    

# Navegando pelo JSON. Dados do do HC Air Temperature (Temperatura do Ar)
hc = data['data'][6] #Ano - Mês - Dia
hcCode = hc['code'] # Chave primária
hcName = hc['name']
hcUnit = hc['unit']
lastDayAvg = hc['values']['avg'][6]
lastDayMax = hc['values']['max'][6]
lastDayMin = hc['values']['min'][6]
lastUpdate = data['dates'][6]

# Convertendo data para unix timestamp
lastUpdate = lastUpdate.replace('-', '/')
formato = "%Y/%m/%d %H:%M:%S"
aux = datetime.strptime(lastUpdate, formato)
lastUpdateUnix = aux.timestamp()

'''
print('Dispositivo de leitura de temperatura do ar')
print(f'Nome do dispositivo: {hcName}')
print(f'Código do dispositivo: {hcCode}') #Chave primária
print(f'Unidade: {hcUnit}')
print(f'Temperatura média do dia anterior: {lastDayAvg}')
print(f'Temperatura máxima do dia anterior: {lastDayMax}')
print(f'Temperatura mínima do dia anterior: {lastDayMin}')
print(f'Horário de última atualização: {lastUpdate}')
print(f'Em Unix: {lastUpdateUnix}')
'''

if __name__ == "__main__":

    #test if the city name was informed as argument
    if len(sys.argv) != 1: # o primeiro  argumento sempre vai ser o chamado do python
        print("Usage:",sys.argv[0])
        exit(1)

    # ------ PEGANDO O HORÁRIO DE EXECUÇÃO DO CLIENTE --------
    # Horário de execução do cliente em unix
    timestampCliente = time.time()
    print(f'Horário de execução do cliente em UNIX: {timestampCliente}')

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
            args=[str(hcCode), hcName, str(hcUnit), str(lastDayAvg), str(lastDayMax), str(lastDayMin), str(lastUpdateUnix)],
            fcn= 'InsertHCData',
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
        args=[str(hcCode), str(lastUpdateUnix)],
        fcn= 'ReadHCData',
        cc_name=cc_name,
        wait_for_event=True,  # optional, for private data
        # for being sure chaincode invocation has been commited in the ledger, default is on tx event
        #cc_pattern="^invoked*"  # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
        ))
    print(response)

