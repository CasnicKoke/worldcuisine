WorldCuisine — nieuwe receptpagina

Kopieer deze drie bestanden naar de hoofdmap van je project:
- recepten.html  (vervangt het oude proefbestand)
- recept.js      (vervangt het oude proefbestand)
- recept-detail.css (nieuw)

De bestaande links in data/recepten/index.json wijzen al naar
recepten.html?id=...; je hoeft recepten.js, worldmap.js en de 166 JSON-bestanden
niet aan te passen.

Test via VS Code Live Server:
  http://127.0.0.1:5500/recepten.html?id=rendang
(pas de poort aan als jouw Live Server een andere gebruikt).

Foto, titel, beschrijving, bereidingstijd, 4 porties, moeilijkheid,
ingrediënten, genummerde stappen en bron worden uit JSON gelezen.
Onbekende bereidingstijd/moeilijkheid worden weggelaten.
Een lege bron wordt niet verzonnen of getoond.

Let op: het bestaande Rendang-JSON heeft een korte, nog onvolledige
proefversie van de ingrediënten en stappen. Vul deze later aan met een
geverifieerd recept en juiste bron.
