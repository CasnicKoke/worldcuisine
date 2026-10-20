# WorldCuisine: indexering van recepten

Kopieer `scripts/` en `data/` naar de hoofdmap van je WorldCuisine-project.
De bestaande `recepten.js` en `worldmap.js` blijven ongewijzigd.

## Indexen genereren

Open Terminal in VS Code, in de hoofdmap van WorldCuisine:

```bash
python3 scripts/build-recepten.py
```

De generator leest elk `data/recepten/<sleutel>.json`-bestand (behalve `index.json`) en schrijft:
- `data/recepten/index.json`
- `data/regio-recepten.json`

Controle of de indexen actueel zijn, zonder bestanden te veranderen:

```bash
python3 scripts/build-recepten.py --check
```

## Recept toevoegen

1. Maak bijvoorbeeld `data/recepten/nieuwGerecht.json`.
2. Geef het `sleutel: "nieuwGerecht"`, de verplichte kaartvelden `titel`, `korteBeschrijving`, `afbeelding`, `url`, plus `regios`.
3. Voeg `volgorde` toe: een uniek nummer, bijvoorbeeld 166.
4. Voeg `regioVolgorde` toe: een object met voor elke regio een uniek volgnummer, bv. `{"mediterraans": 4}`. Dit bepaalt de volgorde binnen die regio.
5. Voer `python3 scripts/build-recepten.py` uit. De indexen worden automatisch bijgewerkt.
6. Controleer op Live Server; commit en push de nieuwe receptfile én beide gegenereerde indexen. GitHub Pages voert geen Python-buildscript uit.

## Veiligheid en compatibiliteit

- De website blijft `data/recepten/index.json` en `data/regio-recepten.json` laden, dus de bestaande JS-bestanden hoeven niet te veranderen.
- Het script controleert sleutel/bestandsnaam, verplichte velden, dubbele sleutel-/volgorde-nummers en regio-posities; bij fouten worden geen indexbestanden geschreven.
- `volgorde` en `regioVolgorde` zijn alleen beheervelden, niet bedoeld om rechtstreeks op de site te tonen.
- De initiële metadata is uit de originele indexen gehaald om de bestaande sortering te behouden.
