#from loginscript import get_hdntl
from cdntoken import get_cdn_token
from sessiontoken import get_session_token
import subprocess
import random
import re
#hdntl = get_hdntl()
hdntl = "example"
sessiontoken = get_session_token()
COMPANY = "channels"
#ORIGIN_FLOW = ["edge-live01-ros", "edge-live02-mun", "edge2-ccast-sl", "edge-mix04-coe", "edge-mix05-coe"] 
ORIGIN_FLOW = ["edge-live12-sl","edge7-ccast-sl"] 
DATABASE_PATH = COMPANY + "_database_v2.txt"
M3U_PATH = COMPANY + ".m3u"
DUMMY = "https://nothingness.com/live.m3u8"
ORIGIN = "\"https://www.directvgo.com\""
USER_AGENT = "\"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0\""
#URLTVG = "url-tvg=\"https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml.gz\""
URLTVG = ""
f = open(DATABASE_PATH,'r')
content = f.read().strip().split('\n')

extinf = "#EXTM3U " + URLTVG + " catchup-type=\"append\" refresh=\"10\" url-logo=\"https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/\" billed-msg=\"Bienvenido a Futbol Max\"\n"
category = ""
for line in content:
    if "Categoria" in line:
        category = line.split(';')
        group = "\"" + category[1] + "\""
        logo_group = "\"" + category[2] + "\""
        set_logo = True
    elif line == '' or line[0] == '#':
        pass
    else:
        line_list = line.split(';')
        if set_logo:
            extinf = extinf + "#EXTINF:-1 tvg-id=\"" + line_list[3] + "\" tvg-logo=\"" + line_list[4] + "\" group-title=" + group + " group-logo=" +  logo_group + "," + line_list[0] + "\n"
            set_logo = False
        else:
            extinf = extinf + "#EXTINF:-1 tvg-id=\"" + line_list[3] + "\" tvg-logo=\"" + line_list[4] + "\" group-title=" + group + "," + line_list[0] + "\n"
        if "https" not in line_list[1]:
            if "*php" in line_list[1]:
                mpd = DUMMY 
            else:
                mpd_list = line_list[1].split(',')
                #extinf = extinf + "#EXTHTTP:{\"Origin\":\"https://portal.app.flow.com.ar\", \"User-Agent\":" + USER_AGENT + "}\n"
                extinf = extinf + "#KODIPROP:inputstream.adaptive.stream_headers=Origin=https://portal.app.flow.com.ar\n"
                mpd = re.sub(r":443", "", get_cdn_token(mpd_list[1], mpd_list[0], sessiontoken))
                #mpd = "https://edge6-ccast-sl.cvattv.com.ar/tok_" + cdntoken + "/live/c" + mpd_list[1] + "eds/" + mpd_list[0] + "/SA_Live_dash_enc_C/" + mpd_list[0] + ".mpd"
        else:
            if "dtvott" in line_list[1]:
                extinf = extinf + "#EXTHTTP:{\"User-Agent\":" + USER_AGENT + ", \"Origin\":" + ORIGIN + ", \"hdntl\":\"" + hdntl + "\"}\n"
            mpd = line_list[1]
        if line_list[2][0] == "*" or mpd == DUMMY:
            if(mpd == DUMMY):
                extinf += "#EXTATTRFROMURL:https://futbolmax.pro/" + line_list[1][4:] + ".php?live=" + line_list[2] + '\n'
            elif len(line_list[2]) > 1:
                domain = line_list[2][1:]
                extinf = extinf + "#EXTHTTP:{\"User-Agent\":" + USER_AGENT + ", \"Origin\": \"" + domain + "\", \"Referer\":\"" + domain + "/\"}\n"
        else:    
            extinf = extinf + "#KODIPROP:inputstream.adaptive.manifest_type=mpd\n"
            extinf = extinf + "#KODIPROP:inputstream.adaptive.license_type=clearkey\n"
            multiple_keys = line_list[2].split('/')
            if len(multiple_keys) > 1:
                lista_keys = '{'
                i = 0
                for key in multiple_keys:
                    key_split = key.split(':')
                    lista_keys += "\"" + key_split[0] + "\":\"" + key_split[1] + "\""
                    if i != len(multiple_keys)-1:
                        lista_keys += ","
                    i += 1

                lista_keys += '}'
                extinf = extinf + "#KODIPROP:inputstream.adaptive.license_key=" + lista_keys + '\n'
            else:    
                extinf = extinf + "#KODIPROP:inputstream.adaptive.license_key=" + line_list[2] + '\n'
        extinf = extinf + mpd + '\n'
with open(M3U_PATH,'w') as output:
    output.write(extinf)

# 2. Agregar archivo al repositorio
subprocess.run(["git", "add", "channels.m3u"], check=True)

# 3. Commit
subprocess.run(["git", "commit", "-m", "Update channels"], check=True)

# 4. Push
subprocess.run(["git", "push"], check=True)
subprocess.run(["exit"], check=True)
#print(extinf)
