import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://portal.app.flow.com.ar/',
    'x-request-id': 'Flow|WEB|4.25.2|999900002429010|95a2d18cb64356d2730b790f464bbfdd|3562637310',
    'tr-log-deviceId': '95a2d18cb64356d2730b790f464bbfdd',
    'tr-log-deviceType': 'cloud_client',
    'tr-log-profileId': 'flow:999900002429010:P',
    'tr-log-regionId': 'flow:heQZKx8yuNMeBm2a15SDRg',
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

params = {
    'region': 'bklkOggBImCQp3+kUWjJrhVDoBFSFSWjzSVpxbnS96ChubJcYAr+ijxovCNqP1KU/DmaJp5YruW3cd6Pspywr8loIbNR8Ig7I0vXTn0nlbA1kUxhlAdpTsCmJtqOpZkuZxmZBNz6zp8=',
    'categories': 'sDUskYo+FVbYmdd1d4iQjIyP4LSIkO4TErDqGaaP7uaDuYeCXSNwORq+9Jpa6/o4AmncNYTHV0ZjjScuILNgzVrWqL6EAqypz3oVUdoTliN16a6ZpHRt1DNqz130q4+VXXVvr8hYWWyr7qnZ8rRRk1Axp7XHWsfD8arVtrOBmdVAhBlEUpornj3DOR3wbZ++kzLHIzWVnowtXS3oOw05t877oIRwc8hKuOxE89ZYTqhjHESXks3AI8K0wc9HPTC410n8EbCrrhpLPWreFzjKN7hEw365kQUWuYgdo8pMReN+jbn7MC0l0c6mBP2uJzWa4XZIKMjaVbYWNilqDdTr9cGEISXcnAeejJIXM0xUf16fA6pAMBb5XmRn1SzkS+D7va6vHzij/mVXIWFVSQQFlF4yWx2zu1zfOAh+5XGCX95C32Ed7yx7XWJVWNFOAbJuzQCCIG3KslpVqhDQevUtZrHDZ/7WPBs0dP2Hoey7Yz2H4sqeRijunVC5y+jA2JwPd8R/mSinHXBwTOU5qeYG2wruNopLRyH21H4l6aVy8eCu5saZeD488oHZuE09zrHzf+ifb1WzfflTmWAnY5B1cED3cCRFgDaEh/iHsiB9DNFdrsmRsmJ5O4VeUtQsthUXMiHJ9Zq/dQfwnvCz5G6JAv9NXVt1KYap61EwwunWSZE=',
}

response = requests.get(
    'https://cdn.bo.flow.com.ar/content/api/v1/Playback/live/HS22in343LTrv0xkcRc58g',
    params=params,
    headers=headers,
)