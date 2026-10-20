# WorldCuisine — migratie naar JSON

De ZIP bevat de gewijzigde bestanden en de nieuwe `data/`-map. Plaats alle inhoud in de root van je bestaande WorldCuisine-project.

- `recepten.js` vervangt het oude bestand met hardcoded recepten. Het laadt JSON.
- `worldmap.js` vervangt het oude bestand. De regioselectie en startkaarten wachten op de JSON-data.
- `data/recepten/index.json` bevat de kaartgegevens voor alle 166 recepten.
- `data/regio-recepten.json` bevat de originele 42 regio's en hun recepten in originele volgorde.
- `data/recepten/<sleutel>.json` bevat het volledige receptrecord per gerecht.

Het bestaande `worldmap.html` hoeft niet aangepast te worden: de scriptvolgorde blijft `recepten.js` en daarna `worldmap.js`. Bestaande afbeeldingen, titels, beschrijvingen, links en regio-ID's zijn overgenomen. Ook onvolledige voorbeeldteksten zijn bewust niet geredigeerd.

## Testen

1. Maak een back-up van de oude JS-bestanden.
2. Kopieer de twee JS-bestanden en de `data`-map naar de projectroot.
3. Bekijk de site via Live Server in VS Code (niet via `file://`).
4. Test de vier startkaarten, selecteer enkele regio's en kijk of de juiste recepten verschijnen.
5. Controleer de Console op laadfouten. Push daarna naar GitHub.

## Onderhoud

Voor een nieuw gerecht maak je een JSON-bestand, voeg je een record toe in `index.json` en koppel je het aan een regio in `regio-recepten.json`. In een volgende stap kunnen we de index automatisch genereren uit alle losse bestanden zodat onderhoud op één plek mogelijk is.
