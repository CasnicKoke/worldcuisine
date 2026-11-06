#!/usr/bin/env python3
"""Controleer dubbele volgordenummers in World Cuisine recept-JSON's.

Gebruik vanuit de hoofdmap van World Cuisine:
    python3 controleer_volgorde.py
of met expliciete map:
    python3 controleer_volgorde.py data/recepten

Dit programma wijzigt geen bestanden.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys


def lees_recepten(map_pad):
    recepten = []
    fouten = []
    for pad in sorted(map_pad.glob('*.json')):
        if pad.name.lower() == 'index.json':
            continue  # gegenereerde index, geen zelfstandig recept
        try:
            with pad.open(encoding='utf-8-sig') as bestand:
                data = json.load(bestand)
            if not isinstance(data, dict):
                fouten.append(f'{pad.name}: hoofdstructuur is geen object')
                continue
            if not any(k in data for k in ('sleutel', 'titel', 'volgorde', 'regioVolgorde')):
                continue
            recepten.append((pad, data))
        except (OSError, json.JSONDecodeError) as exc:
            fouten.append(f'{pad.name}: {exc}')
    return recepten, fouten


def toon(groep):
    for pad, rec in sorted(groep, key=lambda item: item[0].name.lower()):
        print(f'      - {rec.get("titel", "(zonder titel)")} '
              f'[sleutel: {rec.get("sleutel", "?")}]  bestand: {pad.name}')


def norm_positie(waarde):
    """Maak 3 en '3' vergelijkbaar, maar behoud ongeldige waarden."""
    if waarde is None or isinstance(waarde, bool):
        return None
    if isinstance(waarde, int):
        return str(waarde)
    if isinstance(waarde, str) and waarde.strip():
        tekst = waarde.strip()
        return str(int(tekst)) if tekst.isdecimal() else tekst
    return str(waarde)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('map', nargs='?', default='data/recepten',
                        help='Map met losse recept-JSON-bestanden (standaard: data/recepten)')
    args = parser.parse_args()
    map_pad = Path(args.map)
    if not map_pad.is_dir():
        print(f'FOUT: map niet gevonden: {map_pad.resolve()}')
        print('Start vanuit de hoofdmap van World Cuisine, of geef de juiste map als argument.')
        return 2

    recepten, fouten = lees_recepten(map_pad)
    globaal = defaultdict(list)
    regionaal = defaultdict(list)
    for pad, rec in recepten:
        pos = norm_positie(rec.get('volgorde'))
        if pos is not None:
            globaal[pos].append((pad, rec))
        rv = rec.get('regioVolgorde') or {}
        if isinstance(rv, dict):
            for regio, waarde in rv.items():
                pos = norm_positie(waarde)
                if pos is not None:
                    regionaal[(regio, pos)].append((pad, rec))

    print(f'Gecontroleerd: {len(recepten)} receptbestanden in {map_pad}')
    aantal = 0
    print('\nDUBBELE ALGEMENE VOLGORDE (veld: volgorde)')
    dubbels = [(nr, groep) for nr, groep in globaal.items() if len(groep) > 1]
    if not dubbels:
        print('  Geen dubbele waarden gevonden.')
    for nr, groep in sorted(dubbels, key=lambda x: (not x[0].isdigit(), int(x[0]) if x[0].isdigit() else x[0])):
        print(f'  Volgorde {nr}:')
        toon(groep)
        aantal += 1

    print('\nDUBBELE REGIOVOLGORDE (veld: regioVolgorde)')
    dubbels = [(regio, nr, groep) for (regio, nr), groep in regionaal.items() if len(groep) > 1]
    if not dubbels:
        print('  Geen dubbele waarden gevonden.')
    for regio, nr, groep in sorted(dubbels, key=lambda x: (x[0], not x[1].isdigit(), int(x[1]) if x[1].isdigit() else x[1])):
        print(f'  Regio {regio}, positie {nr}:')
        toon(groep)
        aantal += 1

    if fouten:
        print('\nNIET GELEZEN BESTANDEN')
        for fout in fouten:
            print('  -', fout)
    print(f'\nResultaat: {aantal} conflict(en); {len(fouten)} leesfout(en).')
    print('Er zijn geen bestanden aangepast.')
    return 1 if aantal or fouten else 0


if __name__ == '__main__':
    sys.exit(main())
