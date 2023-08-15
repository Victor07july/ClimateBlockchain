apiURI = 'https://api.fieldclimate.com/v2'
# HMAC Authentication credentials
"""
How to generate your HMAC keys
https://support.metos.at/en/support/solutions/articles/15000018359-create-hmac-api-keys-using-fieldclimate
"""
publicKey = '0b0989163ed6b703cd13904039b4731bea2788e76f51e20f'
privateKey = 'ec07663127f0f862d2fd91d32251b3667fde7c479cf3fd00'

import requests
from requests.auth import AuthBase
#its necessary install these follow library
# pip install pycrypto
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from datetime import datetime
from dateutil.tz import tzlocal
import json

# Class to perform HMAC encoding
class AuthHmacMetos(AuthBase):
    # Creates HMAC authorization header for Metos REST service GET request.
    def __init__(self, apiRoute, publicKey, privateKey, method):
        self._publicKey = publicKey
        self._privateKey = privateKey
        self._method = method
        self._apiRoute = apiRoute

    def __call__(self, request):
        dateStamp = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        request.headers['Request-Date'] = dateStamp
        msg = (self._method + self._apiRoute + dateStamp + self._publicKey).encode(encoding='utf-8')
        h = HMAC.new(self._privateKey.encode(encoding='utf-8'), msg, SHA256)
        signature = h.hexdigest()
        request.headers['Authorization'] = 'hmac ' + self._publicKey + ':' + signature
        return request

""" Example get user information """
def example_get_method():
    endpoint = '/user'
    method = 'GET'
    auth = AuthHmacMetos(endpoint, publicKey, privateKey, method)
    response = requests.get(apiURI+endpoint, headers={'Accept': 'application/json'}, auth=auth)
    json_object = response.json()
    json_formatted = json.dumps(json_object, indent=2)
    print(json_formatted)

""" Example post: response forecast """
def example_post_method():
    stationID = '00206C61'
    """ data_group: raw, hourly or daily """
    data_group = 'hourly'
    """ name: general3 or general7"""
    name = 'general3'
    method = 'POST'
    payload = {"name": name}
    """
     To user forecast you must have a specific license
    """
    endpoint = '/forecast/' + stationID + '/' + data_group
    auth = AuthHmacMetos(endpoint, publicKey, privateKey, method)
    response = requests.post(apiURI+endpoint, headers={'Accept': 'application/json'}, auth=auth, json=payload)
    json_object = response.json()
    json_formatted = json.dumps(json_object, indent=2)
    print(json_formatted)


def getRain():
    url = "https://api.fieldclimate.com/v2/calculation/00206C61/rain"
    method = 'GET'

    payload = "{\n    \"type\": \"rain\",\n    \"ch\": 5,\n    \"date_from\": \"1640995200\",\n    \"date_to\": \"1665791940\"\n}"
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



getRain()
#example_get_method()