import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Referer': 'https://portal.app.flow.com.ar/',
    'x-request-id': 'Flow|WEB|4.25.2|999900002429010|95a2d18cb64356d2730b790f464bbfdd|6203048269',
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
    'userDeviceToken': 'bklkOggBIoABsDUskYo+FVbYmdd1d4iQjIyP4LSIkO4TErDqGaaP7uZm3Nhymnpck7r0j65gjhOtRy+p3mlt+q8CjL9EV+i0n8aT7vZxYsKtPYkJwCQDnbhLH9uNqx+n+V1Dy4Z6j7Okv9CKjaMyH+MHfbZ8GCP1c3Wotjztonb2NB4jJf+Lwec=',
    'profile': 'flow:999900002429010:P',
    'deviceInfo': {
        'appVersion': '4.25.2',
        'brand': 'WEB',
        'casId': '6cd0d791ef4f8042cafba66832f9c08e',
        'model': 'PC',
        'name': 'WEB(Win32)',
        'os': 'WindowsPC',
        'osVersion': '4.25.2',
        'playerType': 'TheoPlayer',
        'type': 'cloud_client',
    },
}

response = requests.post('https://cdn.bo.flow.com.ar/users/node/1/api/v1/session', headers=headers, json=json_data)
response = response.json()
print(response['tokens']['region'])
print(response['tokens'])

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"userDeviceToken":"bklkOggBIoABsDUskYo+FVbYmdd1d4iQjIyP4LSIkO4TErDqGaaP7uZm3Nhymnpck7r0j65gjhOtRy+p3mlt+q8CjL9EV+i0n8aT7vZxYsKtPYkJwCQDnbhLH9uNqx+n+V1Dy4Z6j7Okv9CKjaMyH+MHfbZ8GCP1c3Wotjztonb2NB4jJf+Lwec=","profile":"flow:999900002429010:P","deviceInfo":{"appVersion":"4.25.2","brand":"WEB","casId":"6cd0d791ef4f8042cafba66832f9c08e","model":"PC","name":"WEB(Win32)","os":"WindowsPC","osVersion":"4.25.2","playerType":"TheoPlayer","type":"cloud_client"}}'
#response = requests.post('https://cdn.bo.flow.com.ar/users/node/1/api/v1/session', headers=headers, data=data)