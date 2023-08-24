# https://stackoverflow.com/questions/67906542/search-for-keywords-in-file-directory

import os
import json
from datetime import datetime
import time

stationID = '00206C61'

# leitura do arquivo
with open(f'blockchain/gateway/fieldclimate/json/{stationID}_output.json', 'r') as file:
    jsonFile = json.load(file)    

# pegando o horário mais atual
lastUpdated = jsonFile['dates'][0]
print(lastUpdated)

# navegando para a área de dados (data)
data = jsonFile['data']

# função de escanear dados específicos
def jsonScan(json_object, name):
    objName = name
    objType = [obj for obj in json_object if obj['name']==name][0]['type']
    objUnit = [obj for obj in json_object if obj['name']==name][0]['unit']
    objValues = [obj for obj in json_object if obj['name']==name][0]['values']

    return objName, objType, objUnit, objValues

print(jsonScan(data, "HC Air Temperature"))