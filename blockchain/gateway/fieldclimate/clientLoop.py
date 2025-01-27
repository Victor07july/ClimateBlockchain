import sys
from datetime import datetime
import time
import json
from modules.chaincodeInvoke import invoke
from modules.fieldClimateAPI import APIConnect
from modules.loggerSetup import loggerSetup

# configs de conexão com a rede
domain = ["connection-org1"]
channel_name = "mychannel"
cc_name = "fieldclimate"
cc_version = "1.0"

# ID da estação desejada
#stationID = input('Insira o ID da estação desejada: ')
stationID = '00206C61'

infoLogger = loggerSetup('informar', 'clientLoop_log.txt')

infoLogger.info(f'ID da estação: {stationID}')
infoLogger.info(f'Iniciando loop...')
# repetição do código a cada 5 minutos
try:
    # Loop de execução
    while True:
        infoLogger.info('Procurando arquivo JSON para leitura')
        try:
            # leitura do arquivo json antes de atualizar o arquivo
            with open(f'json/{stationID}_output.json', 'r') as file:
                jsonFile = json.load(file)
            infoLogger.info('Leitura concluída')
        
        except FileNotFoundError as e:
            # caso o arquivo  não seja encontrado    
            print(f'Arquivo {stationID}_output.json não encontrado')
            infoLogger.info.exception(e)
            

        #NAVEGANDO NO JSON \/
        infoLogger.info('Verificando último horário de atualização dos dados no JSON')
        oldLastUpdated = jsonFile['dates'][0]

        # chamando api com o ID da estação inserida, após o chamado o resultado é armazenado em um arquivo json com o nome da estação
        infoLogger.info('Realizando chamada da API')
        APIConnect(stationID)
        infoLogger.info('Chamada realizada com sucesso')

        infoLogger.info(f'Fazendo leitura do novo arquivo {stationID}_output.json')
        # leitura do arquivo json após atualizar o arquivo
        with open(f'json/{stationID}_output.json', 'r') as file:
            jsonFile = json.load(file)    

        infoLogger.info('Comparando horários...')
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
                infoLogger.info('Dados não atualizados.. Reiniciando em 5 minutos')
                time.sleep(300)
            else:
                infoLogger.info('Dados atualizados! Prosseguindo')
                infoLogger.info(f'Horários: {oldLastUpdated} (antigo) {newLastUpdated} (novo)')
                break

        infoLogger.info('Convertendo horário para unix')
        newLastUpdated = newLastUpdated.replace('-', '/')
        formato = "%Y/%m/%d %H:%M:%S"
        aux = datetime.strptime(newLastUpdated, formato)
        lastUpdatedUnix = aux.timestamp()
        print(f'A ultima atualização na estação {stationID} foi em: {newLastUpdated}')
        print(f'Horário em Unix: {lastUpdatedUnix}')

        infoLogger.info('Buscando dados do dispositivo no arquivo {stationID}_output.json')
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
            infoLogger.info('Dispositivo não encontrado em {stationID}_output.json')

        infoLogger.info('Realizando invoke do chaincode com os dados do dispositivo')
        if __name__ == "__main__":

            #test if the city name was informed as argument
            if len(sys.argv) != 1: # o primeiro  argumento sempre vai ser o chamado do python
                print("Usage:",sys.argv[0])
                exit(1)
            
            # # Invocando INSERT
            response = invoke('InsertStationData', stationID, deviceName, deviceType, unit, str(values), str(lastUpdatedUnix), insertTimestamp=True)
            # invoke retorna o response da transação, que deve ser vazio no caso do insert
            if response != '':
                print('Erro ao inserir dados na blockchain. Encerrando cliente.')
                infoLogger.info('Erro ao inserir dados na blockchain. Encerrando cliente.')
                exit(1)

            # # Invocando GET
            invoke('ReadStationData', stationID, deviceName)
    
            print('\n')
            print("Reiniciando código!")
            infoLogger.info('Sucesso! Reiniciando...')

except KeyboardInterrupt:
    print("\nProcesso encerrado pelo usuário")
    infoLogger.info('Processo encerrado pelo usuário')