import requests
import re


proxies = {
    'http': 'http://sptaklusdt:pTL_nok3yDdjg95aH5@ar.decodo.com:10001',
    'https': 'http://sptaklusdt:pTL_nok3yDdjg95aH5@ar.decodo.com:10001',
}
def get_cdn_token(ceds, channel, sessiontoken):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-ES,es;q=0.9',
        'authorization': 'Bearer ' + sessiontoken,
        'origin': 'https://portal.app.flow.com.ar',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'x-request-id': 'Flow|WEB|4.11.1|999900002429010|81586734|5106457104',
    }
    url = f'https://cdn-token.app.flow.com.ar/cdntoken/v1/generator?path=https:%2F%2Fchromecast.cvattv.com.ar%2Flive%2Fc{ceds}eds%2F{channel}%2FSA_Live_dash_enc_C%2F{channel}.mpd'
    response = requests.get(
        url,
        headers=headers,
    #    proxies=proxies,
    )
    print(response)
    json_response = response.json()
    chromecast_url = "https://chromecast.cvattv.com.ar/live/c" + ceds + "eds/" + channel + "/SA_Live_dash_enc_C/" + channel + ".mpd?cdntoken=" + str(json_response["token"])
    print(chromecast_url)
    response2 = requests.get(chromecast_url,
                headers=headers,
            #    proxies=proxies,
                allow_redirects=False)
    #print("CDN Token: ", response2.headers["Location"])
    #print("https://chromecast.cvattv.com.ar/live/c6eds/ESPN2_Arg/SA_Live_dash_enc_C/ESPN2_Arg.mpd?cdntoken=" + str(json_response["token"]))
    #cdntoken = re.search(r"(?<=tok_).*?(?=/live)", response2.headers["Location"]).group(0)
    #print("real token: ", cdntoken)
    print("CDN Token: ", response2.headers["Location"])
    return response2.headers["Location"]
#get_cdn_token("6", "ESPN2_Arg", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjoiOTk5OTAwMDAyNDI5MDEwIiwiZXhwIjoxNzcyMjA0NTE3LCJhY2NvdW50SWQiOiIxMzExNTY0MyIsInJlZ2lvbklkIjoiNDIiLCJkZXZpY2UiOnsiZGV2aWNlSWQiOiI4ODM3MTYxOCIsImRldmljZVR5cGUiOiJjbG91ZF9jbGllbnQiLCJpcEFkZHJlc3MiOiIiLCJkZXZpY2VOYW1lIjoiV0VCKFdpbjMyKSIsIm1hY0FkZHJlc3MiOiI4OEI1QjFFRjM1QUEiLCJzZXJpYWxOdW1iZXIiOiIiLCJzdGF0dXMiOiJBIiwidXVpZCI6Ijg4QjVCMUVGMzVBQUZCN0Q0OTI1MzFCREI5RDFEODU2In0sImRldmljZVRhZ3MiOltdfQ.xpgdK_xyF-SDjA8iGOlRGaP7lKhIgEfqkkLZ7Ns-_BE")