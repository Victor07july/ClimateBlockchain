# https://api.fieldclimate.com/v2/docs#system

import requests
from requests.auth import AuthBase
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from datetime import datetime
from dateutil.tz import tzlocal
from nose.tools import assert_true
import unittest
from unittest.mock import patch, Mock
import unittest

# Variáveis da API
apiURI = 'https://api.fieldclimate.com/v2' # basta escolher se quer a api v1 ou v2

# HMAC Authentication credentials
publicKey = '0b0989163ed6b703cd13904039b4731bea2788e76f51e20f'
privateKey = 'ec07663127f0f862d2fd91d32251b3667fde7c479cf3fd00'

# Service/Route that you wish to call
# Dependendo da chamada, vc precisa mudar o método (GET, POST, etc)
stationID = '00206C61'
apiRoute = f'/data/{stationID}/raw/last/1' #Ultimo dado enviado pela estação / dispositivo

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


# classe para testar a classe AuthHmacMetosGet
class TestAuthHmacMetosGet(unittest.TestCase):

    def test_call(self):
        # dados para mock
        apiRoute = '/test'
        publicKey = 'public_key'
        privateKey = 'private_key'

        # cria uma instancia de mock que simula um request, sem realizar a chamada de um HTTP real
        request = Mock()
        
        # instancia um dicionario vazio de cabeçalhos. será inserido ao fazer a chamada de AuthHmacMetosGet
        request.headers = {}

        # cria uma instancia de AuthHmacMetosGet com a rota e chaves com dados mock
        auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)

        # executa a instancia de auth com o request mockado
        auth(request)

        # os cabeçalhos do request devem ser 'Authorization' e 'Date', que são inseridos pelo AuthHmacMetosGet
        self.assertIn('Authorization', request.headers)
        self.assertIn('Date', request.headers)