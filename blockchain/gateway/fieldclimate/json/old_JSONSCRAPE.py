# https://stackoverflow.com/questions/67906542/search-for-keywords-in-file-directory

import os
import json
from datetime import datetime
import time

with open('blockchain/gateway/fieldclimate/json/general_output.json', 'r') as file:
    jsonFile = json.load(file)    

data = jsonFile['data']

# Navegando pelo JSON. Dados do do HC Air Temperature (Temperatura do Ar)
lastUpdate = jsonFile['dates'][6] # data de ultima atualização #Ano - Mês - Dia
hc = jsonFile['data'][6]  #Dispositivo HC
hcName = hc['name']
hcUnit = hc['unit']
hcCode = hc['code']
lastDayAvg = hc['values']['avg'][6]
lastDayMax = hc['values']['max'][6]
lastDayMin = hc['values']['min'][6]

# Convertendo data para unix timestamp
lastUpdate = lastUpdate.replace('-', '/')
formato = "%Y/%m/%d %H:%M:%S"
aux = datetime.strptime(lastUpdate, formato)
lastUpdateUnix = aux.timestamp()

# Prints
print('Dispositivo de leitura de temperatura do ar')
print(f'Nome do dispositivo: {hcName}')
print(f'Código do dispositivo: {hcCode}') #Chave primária
print(f'Unidade: {hcUnit}')
print(f'Temperatura média do dia anterior: {lastDayAvg}')
print(f'Temperatura máxima do dia anterior: {lastDayMax}')
print(f'Temperatura mínima do dia anterior: {lastDayMin}')
print(f'Horário de última atualização: {lastUpdate}')
print(f'Em Unix: {lastUpdateUnix}')