#!/usr/bin/env python3
"""Bouw de WorldCuisine-indexen uit data/recepten/*.json.

Gebruik: python3 scripts/build-recepten.py
Controle zonder bestanden aan te passen: python3 scripts/build-recepten.py --check
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEPTEN_DIR = ROOT / "data" / "recepten"
INDEX_PAD = RECEPTEN_DIR / "index.json"
REGIOS_PAD = ROOT / "data" / "regio-recepten.json"
KAARTVELDEN = ("titel", "korteBeschrijving", "afbeelding", "url")


def lees_json(pad: Path):
    try:
        return json.loads(pad.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as fout:
        raise ValueError(f"Kan {pad.relative_to(ROOT)} niet lezen: {fout}") from fout


def json_tekst(waarde):
    return json.dumps(waarde, indent=2, ensure_ascii=False) + "\n"


def bouw_indexen():
    records = []
    sleutels = set()
    fouten = []
    bestanden = sorted(RECEPTEN_DIR.glob("*.json"))
    for pad in bestanden:
        if pad == INDEX_PAD:
            continue
        try:
            data = lees_json(pad)
            if not isinstance(data, dict):
                raise ValueError("verwacht een JSON-object")
            sleutel = data.get("sleutel")
            if not isinstance(sleutel, str) or not sleutel.strip():
                raise ValueError("'sleutel' ontbreekt of is ongeldig")
            if sleutel != pad.stem:
                raise ValueError(f"'sleutel' ({sleutel}) is anders dan bestandsnaam ({pad.stem})")
            if sleutel in sleutels:
                raise ValueError(f"dubbele sleutel: {sleutel}")
            if any(not isinstance(data.get(v), str) for v in KAARTVELDEN):
                raise ValueError("ontbrekend/ongeldig kaartveld: titel, korteBeschrijving, afbeelding of url")
            regios = data.get("regios")
            if not isinstance(regios, list) or not regios or any(not isinstance(r, str) or not r for r in regios):
                raise ValueError("'regios' moet een niet-lege lijst met regio-ID's zijn")
            if len(regios) != len(set(regios)):
                raise ValueError("'regios' bevat dubbele regio-ID's")
            volgorde = data.get("volgorde")
            if not isinstance(volgorde, int) or isinstance(volgorde, bool) or volgorde < 0:
                raise ValueError("'volgorde' moet een positief geheel getal of 0 zijn")
            posities = data.get("regioVolgorde")
            if not isinstance(posities, dict) or set(posities) != set(regios):
                raise ValueError("'regioVolgorde' moet voor elke regio precies één positie bevatten")
            if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 for n in posities.values()):
                raise ValueError("regioposities moeten gehele getallen vanaf 0 zijn")
            sleutels.add(sleutel)
            records.append(data)
        except ValueError as fout:
            fouten.append(f"{pad.name}: {fout}")
    if fouten:
        raise ValueError("Ongeldige recepten:\n  - " + "\n  - ".join(fouten))
    if not records:
        raise ValueError("Geen receptbestanden gevonden")
    volgordes = [r["volgorde"] for r in records]
    if len(volgordes) != len(set(volgordes)):
        raise ValueError("'volgorde' is niet uniek; geef elk recept zijn eigen nummer")

    records.sort(key=lambda r: r["volgorde"])
    index = {"schemaVersie": 1, "recepten": {}}
    regios = {}
    for rec in records:
        key = rec["sleutel"]
        index["recepten"][key] = {
            **{veld: rec[veld] for veld in KAARTVELDEN},
            "regios": rec["regios"],
            "bestand": f"data/recepten/{key}.json",
        }
        for regio in rec["regios"]:
            regios.setdefault(regio, []).append((rec["regioVolgorde"][regio], key))
    for regio, items in regios.items():
        nummers = [n for n, _ in items]
        if len(nummers) != len(set(nummers)):
            raise ValueError(f"Regio '{regio}' heeft dubbele regioVolgorde-nummers")
    # Regio's worden gesorteerd op het vroegst voorkomende recept: daarmee
    # blijft de oorspronkelijke regio-volgorde uit de migratie ongewijzigd.
    regios = {
        regio: [key for _, key in sorted(items)]
        for regio, items in sorted(regios.items(), key=lambda pair: min(
            r["volgorde"] for r in records if pair[0] in r["regios"]
        ))
    }
    return index, regios


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="controleer of de indexen actueel zijn")
    args = parser.parse_args()
    try:
        index, regios = bouw_indexen()
    except ValueError as fout:
        print(f"FOUT: {fout}", file=sys.stderr)
        return 1
    bestanden = ((INDEX_PAD, index), (REGIOS_PAD, regios))
    if args.check:
        fout = False
        for pad, obj in bestanden:
            if not pad.exists() or lees_json(pad) != obj:
                print(f"NIET ACTUEEL: {pad.relative_to(ROOT)}")
                fout = True
        if fout:
            print("Draai: python3 scripts/build-recepten.py")
            return 1
        print(f"OK: {len(index['recepten'])} recepten, {len(regios)} regio's; indexen actueel.")
        return 0
    for pad, obj in bestanden:
        pad.parent.mkdir(parents=True, exist_ok=True)
        pad.write_text(json_tekst(obj), encoding="utf-8")
        print(f"Gegenereerd: {pad.relative_to(ROOT)}")
    print(f"Klaar: {len(index['recepten'])} recepten en {len(regios)} regio's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
