import json

f = open("channels_database_v2.txt", 'r', encoding='utf-8')
content = f.read().strip().split('\n')
f.close()

channels = []
for line in content:
    line_list = line.split(';')
    if len(line_list) > 1:
        moreinf = line_list[1].split(',')
        if len(moreinf) > 1:
            key = line_list[2].split(':')
            channels.append({
                "name": line_list[0],
                "ceds": moreinf[1],
                "channelId": moreinf[0],
                "kid": key[0],
                "key": key[1],
                "logoId": line_list[4]
            })

with open("channels.json", "w", encoding="utf-8") as out:
    json.dump(channels, out, ensure_ascii=False, indent=2)

print(f"Generado channels.json con {len(channels)} canales.")