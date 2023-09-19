import sys
from datetime import datetime
import time
import json
from modules.chaincodeInvoke import invoke
from modules.fieldClimateAPI import APIConnect
from modules.loggerSetup import infoLogger

# configs de conexão com a rede
domain = ["connection-org1"]
channel_name = "mychannel"
cc_name = "fieldclimate"
cc_version = "1.0"

# ID da estação desejada
#stationID = input('Insira o ID da estação desejada: ')
stationID = '00206C61'

infoLogger(f'ID da estação: {stationID}')
infoLogger(f'Iniciando loop...')
# repetição do código a cada 5 minutos
try:
    # Loop de execução
    while True:
        infoLogger('Procurando arquivo JSON para leitura')
        try:
            # leitura do arquivo json antes de atualizar o arquivo
            with open(f'json/{stationID}_output.json', 'r') as file:
                jsonFile = json.load(file)
            infoLogger('Leitura concluída')
        
        except FileNotFoundError as e:
            # caso o arquivo  não seja encontrado    
            print(f'Arquivo {stationID}_output.json não encontrado')
            infoLogger.exception(e)
            

        #NAVEGANDO NO JSON \/
        infoLogger('Verificando último horário de atualização dos dados no JSON')
        oldLastUpdated = jsonFile['dates'][0]

        # chamando api com o ID da estação inserida, após o chamado o resultado é armazenado em um arquivo json com o nome da estação
        infoLogger('Realizando chamada da API')
        APIConnect(stationID)
        infoLogger('Chamada realizada com sucesso')

        infoLogger(f'Fazendo leitura do novo arquivo {stationID}_output.json')
        # leitura do arquivo json após atualizar o arquivo
        with open(f'json/{stationID}_output.json', 'r') as file:
            jsonFile = json.load(file)    

        infoLogger('Comparando horários...')
        # pegando o novo horario de atualizacao
        print("Verificando horário de atualização após a chamada")
        newLastUpdated = jsonFile['dates'][0]

        # Loop de verificação, se o horário não mudar ele repete a verificação até que haja uma mudança
        print("Verificando se os dados foram atualizados")
        while True:
            if oldLastUpdated == newLastUpdated:
                print('Os dados ainda não foram atualizados. Aguarde 5 minutos')
                print(f'Data antes da chamada da API: {oldLastUpdated}')
                print(f'Data após a chamada da API: {newLastUpdated}')
                infoLogger('Dados não atualizados.. Reiniciando em 5 minutos')
                time.sleep(300)
            else:
                infoLogger('Dados atualizados! Prosseguindo')
                infoLogger(f'Horários: {oldLastUpdated} (antigo) {newLastUpdated} (novo)')
                break

        infoLogger('Convertendo horário para unix')
        newLastUpdated = newLastUpdated.replace('-', '/')
        formato = "%Y/%m/%d %H:%M:%S"
        aux = datetime.strptime(newLastUpdated, formato)
        lastUpdatedUnix = aux.timestamp()
        print(f'A ultima atualização na estação {stationID} foi em: {newLastUpdated}')
        print(f'Horário em Unix: {lastUpdatedUnix}')

        infoLogger('Buscando dados do dispositivo no arquivo {stationID}_output.json')
        # navegando para a área de dados (data)
        data = jsonFile['data']

        # função de escanear  específicos do json e retornar em variáveis
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
            infoLogger('Dispositivo não encontrado em {stationID}_output.json')

        infoLogger('Realizando invoke do chaincode com os dados do dispositivo')
        if __name__ == "__main__":

            #test if the city name was informed as argument
            if len(sys.argv) != 1: # o primeiro  argumento sempre vai ser o chamado do python
                print("Usage:",sys.argv[0])
                exit(1)

            invoke('InsertStationData')
            invoke('ReadStationData')           

            print('\n')
            print("Reiniciando código!")
            infoLogger('Sucesso! Reiniciando...')

except KeyboardInterrupt:
    print("\nProcesso encerrado pelo usuário")
    infoLogger('Processo encerrado pelo usuário')