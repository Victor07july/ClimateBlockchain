import sys
from hfc.fabric import Client as client_fabric
from hfc.fabric_network.gateway import Gateway
from hfc.fabric_network.network import Network
from hfc.fabric_network.contract import Contract
import asyncio
from datetime import datetime
import time
import json
from fieldClimateAPI import APIConnect

domain = ["connection-org1"]
channel_name = "mychannel"
cc_name = "fieldclimate"
cc_version = "1.0"

# ID da estação desejada
#stationID = input('Insira o ID da estação desejada: ')
stationID = '00206C61'

try:
    while True:
        # leitura do arquivo json antes de atualizar o arquivo
        with open(f'json/{stationID}_output.json', 'r') as file:
            jsonFile = json.load(file)    

        #NAVEGANDO NO JSON \/
        # pegando o horário de atualização antigo
        print("Verificando ultimo horário de atualização")
        oldLastUpdated = jsonFile['dates'][0]

        # chamando api com o ID da estação inserida, após o chamado o resultado é armazenado em um arquivo json com o nome da estação
        print('Realizando chamada da API...')
        APIConnect(stationID)

        # leitura do arquivo json após atualizar o arquivo
        with open(f'json/{stationID}_output.json', 'r') as file:
            jsonFile = json.load(file)    

        # pegando o novo horario de atualizacao
        print("Verificando novo último horário de atualização")
        newLastUpdated = jsonFile['dates'][0]

        # checando se o horário é o mesmo
        print("Verificando se os dados foram atualizados")
        while True:
            if oldLastUpdated == newLastUpdated:
                print('Os dados ainda não foram atualizados. Aguarde 5 minutos')
                print(oldLastUpdated)
                print(newLastUpdated)
                time.sleep(300)
            else:
                print("Os dados da estação foram atualizados! Prosseguindo com a execução")
                break
                  
        # convertendo este horário para unix
        newLastUpdated = newLastUpdated.replace('-', '/')
        formato = "%Y/%m/%d %H:%M:%S"
        aux = datetime.strptime(newLastUpdated, formato)
        lastUpdatedUnix = aux.timestamp()
        print(f'A ultima atualização na estação {stationID} foi em: {newLastUpdated}')
        print(f'Horário em Unix: {lastUpdatedUnix}')

        # navegando para a área de dados (data)
        data = jsonFile['data']

        # função de escanear dados específicos (arquivo e dado desejado)
        # todos os dispositivos do fieldclimate possuem a mesma estrutura
        def jsonScan(json_object, name):
            deviceName = name
            deviceType = [obj for obj in json_object if obj['name']==name][0]['type']
            unit = [obj for obj in json_object if obj['name']==name][0]['unit']
            values = [obj for obj in json_object if obj['name']==name][0]['values']

            return deviceName, deviceType, unit, values

        # chamando a função
        try:
            deviceName, deviceType, unit, values = jsonScan(data, 'HC Air temperature')
        except IndexError:
            print(f"O dispositivo inserido não foi encontrado. Verifique se o nome está correto ou se ele existe na estação {stationID}")

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
                args=[stationID, deviceName, deviceType, unit, str(values), str(lastUpdatedUnix), str(clientExecutionUnix)],
                fcn= 'InsertStationData',
                cc_name=cc_name,
                wait_for_event=True,  # optional, for private data
                # for being sure chaincode invocation has been commited in the ledger, default is on tx event
                #cc_pattern="^invoked*"  # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
                ))
            print(response)
            
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

except KeyboardInterrupt:
    print("\nProcesso encerrado pelo usuário")