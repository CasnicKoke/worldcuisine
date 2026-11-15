#!/usr/bin/env python3
"""Werk de regio-indeling in World Cuisine worldmap.js bij voor Arctische Wereld.

Gebruik vanuit de hoofdmap van de repo:
    python3 patch_arctische_wereld.py
Maakt eerst een back-up: worldmap.js.bak-arctische-wereld
"""
from pathlib import Path
import re

p=Path('worldmap.js')
if not p.exists():
    raise SystemExit('FOUT: worldmap.js niet gevonden. Start dit script in de hoofdmap van je World Cuisine-repository.')
s=p.read_text(encoding='utf-8')
if '"arctische-wereld": ["GL", "Alaska", "Canada-Arctic"]' in s:
    raise SystemExit('Geen wijzigingen nodig: Arctische Wereld staat al in de regio-indeling.')

def replace_once(old, new, label):
    global s
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f'Verwachte structuur voor {label} ontbreekt of is niet uniek (gevonden: {n}). Er is niets opgeslagen.')
    s=s.replace(old,new,1)

# 1. Land-/regio-indeling. Groenland verhuist, Canada en Alaska worden gesplitst in de SVG.
pattern=r'(scandinavie\s*:\s*\[[^\]]*)"GL"\s*,?\s*'
m=re.search(pattern,s)
if not m:
    raise RuntimeError('Groenland niet gevonden bij scandinavie; niets opgeslagen.')
s=s[:m.start()]+m.group(1)+s[m.end():]
replace_once('    canada: ["Canada"],',
'''    "arctische-wereld": ["GL", "Alaska", "Canada-Arctic"],
    canada: ["Canada"],''','regio-indeling')

# 2. Kleurenschema en categorie.
replace_once('    canada: "#C97A73",',
'''    "arctische-wereld": "#76BAC7",
    canada: "#C97A73",''','kleur')
replace_once('    canada: "noord-amerika",',
'''    "arctische-wereld": "noord-amerika",
    canada: "noord-amerika",''','werelddeel')

# 3. Regioteksten. De Arctische Wereld omvat meerdere inheemse keukens.
replace_once('    canada: {\n        titel: "Canada",',
'''    "arctische-wereld": {
        titel: "Arctische Wereld",
        beschrijving:
            "De Arctische Wereld omvat Groenland, Alaska en de drie noordelijke territoria van Canada. De keukens van Inuit, Yupik, Inuvialuit, Dene en andere gemeenschappen zijn sterk verbonden met visvangst, jacht, seizoenen, conservering en lokale ecosystemen. De culturele gebieden lopen deels door de gekozen bestuurlijke grenzen heen.",
        ingredienten:
            "Arctische vis, wild, rendier en kariboe, bessen, zeevruchten, traditioneel geconserveerde producten"
    },

    canada: {
        titel: "Canada",''','regiobeschrijving')

# 4. Ingrediënteniconen: neutrale beschikbare iconen uit World Cuisine.
replace_once('    canada: [\n        { naam: "Zalm", bestand: "icon-fish.png" },',
'''    "arctische-wereld": [
        { naam: "Vis", bestand: "icon-fish.png" },
        { naam: "Wild", bestand: "icon-meat.png" },
        { naam: "Bessen", bestand: "icon-avocado.png" }
    ],

    canada: [
        { naam: "Zalm", bestand: "icon-fish.png" },''','ingrediënteniconen')

# 5. Tijdelijk een bestaande regiophoto gebruiken om kapotte img-URLs te voorkomen.
# Zodra je een passende Arctic-feature maakt, dit vervangen door feature-arctische-wereldAI.jpg.
replace_once('    canada: "feature-canadaAI.jpg",',
'''    "arctische-wereld": "feature-canadaAI.jpg", // tijdelijk; later eigen Arctische feature-afbeelding
    canada: "feature-canadaAI.jpg",''','regiofoto')

backup=Path('worldmap.js.bak-arctische-wereld')
if backup.exists():
    raise SystemExit(f'FOUT: {backup} bestaat al. Verwijder/gebruik bestaande back-up; niets opgeslagen.')
backup.write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
p.write_text(s,encoding='utf-8')
print('Klaar: worldmap.js bijgewerkt. Back-up:', backup)
print('Nieuwe regio: arctische-wereld -> GL, Alaska, Canada-Arctic')
print('Verwijderd uit Noordse Wereld: GL')
