# https://stackoverflow.com/questions/67906542/search-for-keywords-in-file-directory

import os
import json

keywords = ['sk']

def readPath(path):
    for file in os.listdir(path):
        for keyword in keywords:
            if keyword in file:
                #print(file)
                #print(os.path.abspath(file))
                filePath = '../' + path + file
                #filePath = path + file
                #print(filePath)
                #print('')
                return filePath

jsonPath = ''

print("Verificando chaves...")

# Para funcionar no terminal
try:
    with open('connection-org1.json', 'r') as file:
        data = json.load(file)
        jsonPath = 'connection-org1.json'
except FileNotFoundError:
    print('JSON não encontrado. Tentando um caminho alternativo...')
    # Para funcionar no VSCode    
    try:
        with open('blockchain/gateway/connection-org1.json', 'r') as file:
            data = json.load(file)
        jsonPath = 'blockchain/gateway/connection-org1.json'
    except FileNotFoundError:
        print('JSON não encontrado no caminho alternativo.')

else:
    print('JSON encontrado')

###########################
# Orderer Admin private key

# Caminho para o terminal
try:
    filePath = readPath('../organizations/ordererOrganizations/example.com/users/Admin@example.com/msp/keystore/')

except FileNotFoundError:
    print('Chave privada do Admin de Orderer não encontrada. Tentando um caminho alternativo...')
    
    # Caminho para o VSCode
    try:
        filePath = readPath('blockchain/organizations/ordererOrganizations/example.com/users/Admin@example.com/msp/keystore/')

    except FileNotFoundError:
        print('Chave privada do Admin de Orderer não encontrada no caminho alternativo.')

else:
    print('Chave privada do Admin de Orderer encontrada')

data['organizations']['orderer.example.com']['users']['Admin']['private_key'] = filePath
with open(jsonPath, 'w') as file:
    json.dump(data, file, indent=2)

########################
# Org1 Admin private key
try:
    filePath = readPath('../organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/')

except FileNotFoundError:
    print('Chave privada do Admin de Org1 não encontrada. Tentando um caminho alternativo...')
    
    try:
        filePath = readPath('blockchain/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/')

    except FileNotFoundError:
        print('Chave privada do Admin de Org1 não encontrada no caminho alternativo.')

else:
    print('Chave privada do Admin de Org1 encontrada')


data['organizations']['org1.example.com']['users']['Admin']['private_key'] = filePath
with open(jsonPath, 'w') as file:
    json.dump(data, file, indent=2)

#######################
# Org1 User private key
try:
    filePath = readPath('../organizations//peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/')

except FileNotFoundError:
    print('Chave privada do User de Org1 não encontrada. Tentando um caminho alternativo...')
    
    try:
        filePath = readPath('blockchain/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/')

    except FileNotFoundError:
        print('Chave privada do User de Org1 não encontrada no caminho alternativo.')

else:
    print('Chave privada do User de Org1 encontrada')


data['organizations']['org1.example.com']['users']['User1']['private_key'] = filePath
with open(jsonPath, 'w') as file:
    json.dump(data, file, indent=2)

########################
# Org2 Admin private key
try:
    readPath('../organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp/keystore/')

except FileNotFoundError:
    print('Chave privada do Admin de Org2 não encontrada. Tentando um caminho alternativo...')
    
    try:
        readPath('blockchain/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp/keystore/')

    except FileNotFoundError:
        print('Chave privada do Admin de Org2 não encontrada no caminho alternativo.')

else:
    print('Chave privada do Admin de Org2 encontrada')


data['organizations']['org2.example.com']['users']['Admin']['private_key'] = filePath
with open(jsonPath, 'w') as file:
    json.dump(data, file, indent=2)

######################
# Org2 User private key
try:
    readPath('../organizations/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/')

except FileNotFoundError:
    print('Chave privada do User de Org2 não encontrada. Tentando um caminho alternativo...')
    
    try:
        readPath('blockchain/organizations/peerOrganizations/org2.example.com/users/User1@org2.example.com/msp/keystore/')

    except FileNotFoundError:
        print('Chave privada do User de Org2 não encontrada no caminho alternativo.')

else:
    print('Chave privada do User de Org2 encontrada')


data['organizations']['org2.example.com']['users']['User1']['private_key'] = filePath
with open(jsonPath, 'w') as file:
    json.dump(data, file, indent=2)

#print('Caminhos atualizdos com sucesso!')