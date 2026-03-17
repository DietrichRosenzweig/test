
import requests
proxies = {
    'http': 'http://user-sptaklusdt-country-ar-city-rosario:pTL_nok3yDdjg95aH5@gate.decodo.com:10001',
    'https': 'http://user-sptaklusdt-country-ar-city-rosario:pTL_nok3yDdjg95aH5@gate.decodo.com:10001',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Referer': 'https://portal.app.flow.com.ar/',
    'x-request-id': 'Flow|TEND-WEB|1.5.0|999900002429010|88371618|6077213023',
    'Origin': 'https://portal.app.flow.com.ar',
    'DNT': '1',
    'Sec-GPC': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = {
    'deviceToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjoiOTk5OTAwMDAyNDI5MDEwIiwiZXhwIjowLCJkZXZpY2VJZCI6Ijg4MzcxNjE4IiwibWFjQWRkcmVzcyI6Ijg4YjViMWVmMzVhYSJ9.5NOmBVgIorBvBsfQnNxNyTL3iq9legYKlPWmi9tEh54',
    'deviceInfo': {
        'networkType': 'Broadband',
        'playerType': 'TheoPlayer',
        'deviceOsVersion': '1.5.0',
        'casId': 'e825143eaa6c6d5c0d43b019bf931fd7',
        'deviceModel': 'PC',
        'mac': '88b5b1ef35aa',
        'prmDeviceOs': 'WindowsPC',
        'deviceName': 'WEB(Win32)',
        'appVersion': '4.25.1',
        'deviceType': 'cloud_client',
        'deviceBrand': 'WEB',
        'deviceOs': 'WindowsPC',
        'firmwareVersion': '4.25.1',
        'uuid': '88b5b1ef35aafb7d492531bdb9d1d856',
        'ipAddress': '',
    },
}
def get_session_token():
    response = requests.post(
        'https://geo.mnedge.cvattv.com.ar:4446/xtv-ws-client/api/v1/session/13115643',
        headers=headers,
        json=json_data,
    #    proxies=proxies,
    )
    print(response)
    print(response.text)
    sessiontoken = response.headers['Authorization'].split(' ')[1]
    print(sessiontoken)
    return sessiontoken
get_session_token()