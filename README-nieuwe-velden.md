# WorldCuisine — nieuwe receptvelden

Deze map bevat alle 166 individuele JSON-recepten, uitgebreid met:

- `porties`: 4 (standaard voor elk recept)
- `bereidingstijdMinuten`: `null` zolang niet bekend (geheel aantal minuten wanneer bekend)
- `moeilijkheid`: `null` zolang niet bekend (later bijvoorbeeld `makkelijk`, `gemiddeld`, `moeilijk`)
- `ingredienten`: bestaande waarde behouden; bij ontbrekende informatie een lege lijst `[]`
- `bereiding`: bestaande waarde behouden; bij ontbrekende informatie een lege lijst `[]`
- `bron`: object met `receptTitel`, `auteur`, `kookboek` en `url`, allemaal `null` zolang niet geverifieerd

**Let op:** bij `sateAjam.json`, `gadoGado.json` en `nasiGoreng.json` stonden al proefteksten (`geen idee doe maar wat`) in de ingrediënten/bereiding. Die zijn bewust niet stilzwijgend gewijzigd; vervang ze met echte gegevens voor publicatie.

Bij `rendang.json` waren er wel voorbeeldingrediënten en stappen. Ook die zijn letterlijk behouden, niet op juistheid gecontroleerd.

### Installatie

1. Maak een back-up van `data/recepten`.
2. Kopieer alle 166 recepten-JSON's uit deze ZIP naar `data/recepten`, met overschrijven van de bestaande individuele bestanden. De `index.json` en `regio-recepten.json` hoef je niet apart te wijzigen.
3. In VS Code Terminal: `python3 scripts/build-recepten.py --check`.
4. Later, als je de recepten inhoudelijk wijzigt: `python3 scripts/build-recepten.py`.

Je bestaande `recepten.js`, `worldmap.js` en HTML hoeven hiervoor niet te veranderen. Het indexeringsscript houdt de nieuwe detailvelden buiten de lichte kaartenindex, zodat de bestaande weergave behouden blijft.

De bronvermelding mag alleen getoond worden als er daadwerkelijk een geverifieerde bron is ingevoerd; druk geen fictieve of lege verwijzing af.

*Opmerking*: de bestaande link `recepten.html?id=...` is behouden. Die vervangen we wanneer we de nieuwe recepten-detailpagina bouwen.
