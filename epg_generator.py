#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera epg.json con 7 días de programación de todos los canales de
channels.json que tienen epgId.

Formato de salida (claves cortas para minimizar tamaño):
  { "<epgId>": [ { "n": título, "s": startMs, "e": endMs,
                   "sd": "HH:mm", "ed": "HH:mm", "p": programId,
                   "g": [género] }, ... ], ... }

Uso:
    python epg_generator.py

Después de generado, subí epg.json a Codeberg para que la app lo descargue.
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta, timezone

# ── Configuración ─────────────────────────────────────────────────────────────

CHANNELS_URL       = "https://codeberg.org/dietrichrosenzweig/tvarg/raw/branch/main/channels.json"
SCHEDULE_BASE      = "https://cdn.bo.flow.com.ar/content/api/v1/Channel/"
REGION_SESSION_URL = "https://cdn.bo.flow.com.ar/users/node/1/api/v1/session"
OUTPUT_FILE        = "epg.json"
THROTTLE_SECS      = 0.7   # 700ms entre requests para evitar 429
AR_TZ              = timezone(timedelta(hours=-3))

# ── Headers ───────────────────────────────────────────────────────────────────

REGION_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
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
}

REGION_BODY = {
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

SCHEDULE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://portal.app.flow.com.ar/',
    'Origin': 'https://portal.app.flow.com.ar',
    'DNT': '1',
    'Sec-GPC': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
    'x-request-id': 'Flow|WEB|4.25.2|999900002429010|9bbb8417efe830024190f485c0be1872|3615742543',
    'tr-log-deviceId': '9bbb8417efe830024190f485c0be1872',
    'tr-log-deviceType': 'cloud_client',
    'tr-log-profileId': 'flow:999900002429010:P',
    'tr-log-regionId': 'flow:heQZKx8yuNMeBm2a15SDRg',
}

# ── Funciones ─────────────────────────────────────────────────────────────────

def get_region() -> str:
    resp = requests.post(REGION_SESSION_URL, headers=REGION_HEADERS, json=REGION_BODY, timeout=15)
    resp.raise_for_status()
    return resp.json()['tokens']['region']


def week_range():
    """Devuelve (gt, lt) cubriendo 7 días desde hoy 00:00 hora Argentina (UTC-3)."""
    ar_tz   = timezone(timedelta(hours=-3))
    now_ar  = datetime.now(ar_tz)
    start   = now_ar.replace(hour=0, minute=0, second=0, microsecond=0)
    end     = start + timedelta(days=7)
    fmt     = '%Y-%m-%dT%H:%M:%S.000Z'
    return (
        start.astimezone(timezone.utc).strftime(fmt),
        end.astimezone(timezone.utc).strftime(fmt),
    )


def fetch_schedule(epg_id: str, region: str, gt: str, lt: str) -> list:
    params = {
        'page':              '0',
        'size':              '1000',   # 7 días × ~20 prog/día = ~140; 200 cubre de sobra
        'sort':              'start',
        'images':            'S_DESC',
        'filter[end][gt]':   gt,
        'filter[start][lt]': lt,
        'region':            region,
    }
    url = f"{SCHEDULE_BASE}{epg_id}/schedules"
    wait = 10  # segundos iniciales de espera ante 429
    while True:
        resp = requests.get(url, headers=SCHEDULE_HEADERS, params=params, timeout=20)
        if resp.status_code == 429:
            print(f"  ⚠ 429 – esperando {wait}s...", end=' ', flush=True)
            time.sleep(wait)
            wait = min(wait * 2, 120)   # backoff exponencial hasta 2 min
            continue
        resp.raise_for_status()
        return resp.json().get('data', [])


def iso_to_ms(iso_str: str) -> int:
    """'2026-02-28T07:00:00.000Z' → epoch milliseconds (int)"""
    dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def iso_to_display(iso_str: str) -> str:
    """'2026-02-28T07:00:00.000Z' → 'HH:mm' en hora Argentina (UTC-3)"""
    dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    return dt.astimezone(AR_TZ).strftime('%H:%M')


def build_json(channels: list, schedules: dict) -> str:
    """
    Construye el dict epgId → [programas] con claves cortas y lo serializa a JSON.
    Claves: n=título, s=startMs, e=endMs, sd=startDisplay, ed=endDisplay,
            p=programId, g=[géneros]
    """
    root = {}
    for ch in channels:
        epg_id = ch.get('epgId', '')
        if not epg_id:
            continue
        progs = []
        for prog in schedules.get(epg_id, []):
            name_obj = prog.get('name', {})
            title = (name_obj.get('es') or name_obj.get('en', '')) if isinstance(name_obj, dict) else ''
            if not title:
                continue
            start = prog.get('start', '')
            end   = prog.get('end',   '')
            if not (start and end):
                continue

            entry = {
                'n':  title,
                's':  iso_to_ms(start),
                'e':  iso_to_ms(end),
                'sd': iso_to_display(start),
                'ed': iso_to_display(end),
            }

            prog_id = prog.get('id', '')
            if prog_id:
                entry['p'] = prog_id

            genres = []
            for g in prog.get('genres', []):
                genre_text = (g.get('es') or g.get('en', '')) if isinstance(g, dict) else ''
                if genre_text:
                    genres.append(genre_text)
            if genres:
                entry['g'] = genres

            progs.append(entry)

        if progs:
            root[epg_id] = progs

    return json.dumps(root, ensure_ascii=False, separators=(',', ':'))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== TVArg EPG Generator ===\n")

    # 1. Region token fresco
    print("1/4  Obteniendo region token...")
    try:
        region = get_region()
        print(f"     OK ({region[:28]}...)")
    except Exception as e:
        print(f"     ERROR: {e}")
        sys.exit(1)

    # 2. Channels
    print("2/4  Descargando channels.json...")
    try:
        channels = requests.get(CHANNELS_URL, timeout=15).json()
    except Exception as e:
        print(f"     ERROR: {e}")
        sys.exit(1)
    with_epg = [ch for ch in channels if ch.get('epgId')]
    print(f"     {len(with_epg)}/{len(channels)} canales con epgId")

    # 3. Schedules (7 días) — fetch_schedule reintenta indefinidamente ante 429
    gt, lt = week_range()
    print(f"3/4  Fetching schedules [{gt} → {lt}]")
    schedules = {}

    for i, ch in enumerate(with_epg, 1):
        epg_id = ch['epgId']
        print(f"     [{i:3}/{len(with_epg)}] {ch['name'][:35]:<35}", end=' ', flush=True)
        try:
            progs = fetch_schedule(epg_id, region, gt, lt)
            schedules[epg_id] = progs
            print(f"{len(progs):3} prog")
        except Exception as e:
            print(f"FAIL ({e})")
            schedules[epg_id] = []
        time.sleep(THROTTLE_SECS)

    # 4. Generar JSON
    print("4/4  Generando epg.json...")
    json_content = build_json(channels, schedules)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(json_content)

    total = sum(len(v) for v in schedules.values())
    size  = len(json_content.encode('utf-8')) / 1024
    print(f"\n✓  {OUTPUT_FILE} listo: {len(schedules)} canales · {total} programas · {size:.0f} KB")
    print("   Subí el archivo a Codeberg para que la app lo descargue.")


if __name__ == '__main__':
    main()
