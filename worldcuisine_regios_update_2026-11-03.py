#!/usr/bin/env python3
"""Pas de WorldCuisine-regio's aan in worldmap.js.

Gebruik: plaats dit script in de hoofdmap van WorldCuisine en voer uit:
    python3 pas_regios_eurazie_aan.py

Het script behoudt de bestaande interne regiocodes, zodat receptlinks intact blijven.
"""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
bestand = root / "worldmap.js"
if not bestand.is_file():
    raise SystemExit("FOUT: Plaats dit script naast worldmap.js in de hoofdmap van worldcuisine.")

tekst = bestand.read_text(encoding="utf-8")
# Ook geschikt als de vorige versie van dit script al is uitgevoerd.
titel_varianten = [
    'titel: "Noord-Eurazië"',
    'titel: "Oost-Europa en Noord-Azië"',
    'titel: "Noordoost-Europa en Noord-Azië"',
]
gevonden = [titel for titel in titel_varianten if tekst.count(titel) == 1]
if len(gevonden) != 1 or sum(tekst.count(titel) for titel in titel_varianten) != 1:
    raise SystemExit("FOUT: Kon de bestaande titel van de Eurazië-regio niet eenduidig bepalen.")
huidige_titel = gevonden[0]
vervangingen = [
    (
        '"rus-eurazie": ["Russian Federation", "BY", "UA", "MD", "MN", "EE", "LV", "LT"]',
        '"rus-eurazie": ["Russian Federation", "BY", "UA", "MD", "EE", "LV", "LT"]',
    ),
    (
        '"centraal-aziatisch": [ "KZ", "UZ", "KG", "TJ", "TM"]',
        '"centraal-aziatisch": [ "KZ", "UZ", "KG", "TJ", "TM", "MN"]',
    ),
    (
        huidige_titel,
        'titel: "Noordoost-Europa en Noord-Azië"',
    ),
    (
        '"Deze keuken is gevormd door lange winters, landbouwtradities en invloeden uit de Euraziatische steppe."',
        '"Deze culinaire regio omvat Rusland, Oekraïne, Belarus, Moldavië en de Baltische landen. Lange winters, visserij, landbouw en conservering hebben de uiteenlopende regionale keukens gevormd. Polen en de Balkan komen elders in WorldCuisine aan bod."',
    ),
    (
        'titel: "Centraal-Azië"',
        'titel: "Centraal-Azië en Mongolië"',
    ),
    (
        '"Een keuken met sterke nomadische wortels waarin vlees, zuivel en graanproducten centraal staan."',
        '"De keukens van Centraal-Azië en Mongolië delen invloeden van nomadische steppeculturen, met een belangrijke rol voor vlees, zuivel, graanproducten en deeggerechten."',
    ),
]

nieuwe_tekst = tekst
reeds = 0
aangepast = 0
for oud, nieuw in vervangingen:
    oud_aantal = nieuwe_tekst.count(oud)
    nieuw_aantal = nieuwe_tekst.count(nieuw)
    if oud == nieuw and oud_aantal == 1:
        reeds += 1
    elif oud_aantal == 1 and nieuw_aantal == 0:
        nieuwe_tekst = nieuwe_tekst.replace(oud, nieuw, 1)
        aangepast += 1
    elif oud_aantal == 0 and nieuw_aantal == 1:
        reeds += 1
    else:
        raise SystemExit(
            f"FOUT: Verwachte tekst niet precies eenmaal gevonden. Geen bestand gewijzigd.\n"
            f"Gezocht: {oud}\nOud: {oud_aantal}, nieuw: {nieuw_aantal}"
        )

if aangepast:
    backup = root / "worldmap.js.bak"
    if not backup.exists():
        shutil.copy2(bestand, backup)
    bestand.write_text(nieuwe_tekst, encoding="utf-8")

# Controleer de landenlijst en de titels in het resultaat.
assert '"rus-eurazie": ["Russian Federation", "BY", "UA", "MD", "EE", "LV", "LT"]' in nieuwe_tekst
assert '"centraal-aziatisch": [ "KZ", "UZ", "KG", "TJ", "TM", "MN"]' in nieuwe_tekst
assert 'titel: "Noordoost-Europa en Noord-Azië"' in nieuwe_tekst
assert 'titel: "Centraal-Azië en Mongolië"' in nieuwe_tekst
print(f"Klaar: {aangepast} wijzigingen aangebracht; {reeds} waren al aanwezig.")
print("De regiocodes rus-eurazie en centraal-aziatisch zijn behouden.")
print("De receptenindex hoeft niet opnieuw opgebouwd te worden: er zijn geen receptgegevens veranderd.")
