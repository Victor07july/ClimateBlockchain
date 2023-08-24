# https://api.fieldclimate.com/v2/docs#system

import requests
from requests.auth import AuthBase
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from datetime import datetime
from dateutil.tz import tzlocal
import json

def APIConnect(stationID='00206C61'):

    # Class to perform HMAC encoding
    class AuthHmacMetosGet(AuthBase):
        # Creates HMAC authorization header for Metos REST service GET request.
        def __init__(self, apiRoute, publicKey, privateKey):
            self._publicKey = publicKey
            self._privateKey = privateKey
            self._method = 'GET'
            self._apiRoute = apiRoute

        def __call__(self, request):
            dateStamp = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            print("timestamp: ", dateStamp)
            request.headers['Date'] = dateStamp
            msg = (self._method + self._apiRoute + dateStamp + self._publicKey).encode(encoding='utf-8')
            h = HMAC.new(self._privateKey.encode(encoding='utf-8'), msg, SHA256)
            signature = h.hexdigest()
            request.headers['Authorization'] = 'hmac ' + self._publicKey + ':' + signature
            return request


    # Endpoint of the API, version for example: v1
    apiURI = 'https://api.fieldclimate.com/v2' # basta escolher se quer a api v1 ou v2

    # HMAC Authentication credentials
    publicKey = '0b0989163ed6b703cd13904039b4731bea2788e76f51e20f'
    privateKey = 'ec07663127f0f862d2fd91d32251b3667fde7c479cf3fd00'

    # Service/Route that you wish to call
    # Dependendo da chamada, vc precisa mudar o método (GET, POST, etc)
    apiRoute = f'/data/{stationID}/raw/last/1' #Ultimo dado enviado pela estação / dispositivo

    auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)

    if response.status_code == 200:
        print("Conexão com a API FieldClimate realizada com sucesso!")
        print(f"Código: {response.status_code}")
    elif response.status_code != 200:
        print(f"Um erro ocorreu ao buscar a estação. O ID inserido ({stationID}) está correto?")
        print(response.status_code)
        exit()


    # salvar resposta da rota em um arquivo
    json_object = json.dumps(response.json(), indent=4)

    with open(f"json/{stationID}_output.json", "w") as outfile:
        outfile.write(json_object)

    print(f"Os dados da estação foram gravados no arquivo {stationID}_output.json")

    #print(response.json())
    #print(json_object)

    #print(json.dumps(response.json(), indent=2))