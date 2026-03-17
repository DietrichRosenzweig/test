

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Referer': 'https://portal.app.flow.com.ar/',
    'Origin': 'https://portal.app.flow.com.ar',
    'DNT': '1',
    'Sec-GPC': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = {
    'userDeviceToken': 'bklkOggBIoABsDUskYo+FVbYmdd1d4iQjIyP4LSIkO4TErDqGaaP7uZm3Nhymnpck7r0j65gjhOt4t9mBaFYuQ9HGMFDB8UyoCijismefqtfrw9b2qUu19OwegiL/WYtLCDjNyH6U8KwM7B1txrzPOB1Et+efqbyzSErTVfkZeQPQJ4zdoFrPZU=',
    'profile': 'flow:999900002429010:P',
    'deviceInfo': {
        'name': 'WE',
        'playerType': 'TheoPlayer',
        'type': 'cloud_client',
    },
}

response = requests.post('https://cdn.bo.flow.com.ar/users/node/1/api/v1/session', headers=headers, json=json_data)
print(response)
print(response.text)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"userDeviceToken":"bklkOggBIoABsDUskYo+FVbYmdd1d4iQjIyP4LSIkO4TErDqGaaP7uZm3Nhymnpck7r0j65gjhOt4t9mBaFYuQ9HGMFDB8UyoCijismefqtfrw9b2qUu19OwegiL/WYtLCDjNyH6U8KwM7B1txrzPOB1Et+efqbyzSErTVfkZeQPQJ4zdoFrPZU=","profile":"flow:999900002429010:P","deviceInfo":{"appVersion":"4.25.2","brand":"WEB","casId":"5c6132c7f928a3083e20192b432b21bb","model":"PC","name":"WEB(Win32)","os":"WindowsPC","osVersion":"4.25.2","playerType":"TheoPlayer","type":"cloud_client"}}'
#response = requests.post('https://cdn.bo.flow.com.ar/users/node/1/api/v1/session', headers=headers, data=data)

