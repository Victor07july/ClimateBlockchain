import sys
from datetime import datetime
import json
from modules.fieldClimateAPI import APIConnect
from modules.chaincodeInvoke import invoke
from modules.loggerSetup import loggerSetup

domain = ["connection-org1"]
channel_name = "mychannel"
cc_name = "fieldclimate"
cc_version = "1.0"

# ID da estação desejada
#stationID = input('Insira o ID da estação desejada: ')
stationID = '00206C61'

# chamando api com o ID da estação inserida, após o chamado o resultado é armazenado em um arquivo json com o nome da estação
APIConnect(stationID)

# leitura do arquivo json
with open(f'json/{stationID}_output.json', 'r') as file:
    jsonFile = json.load(file)

#NAVEGANDO NO JSON \/
# pegando o horário de atualização dos dados do dispositivo na estação
lastUpdated = jsonFile['dates'][0]
# convertendo este horário para unix
lastUpdated = lastUpdated.replace('-', '/')
formato = "%Y/%m/%d %H:%M:%S"
aux = datetime.strptime(lastUpdated, formato)
lastUpdatedUnix = aux.timestamp()
print(f'A ultima atualização na estação {stationID} foi em: {lastUpdated}')
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

    invoke('InsertStationData', stationID, deviceName, deviceType, unit, str(values), str(lastUpdatedUnix), insertTimestamp=True)
    invoke('ReadStationData', stationID, deviceName)
