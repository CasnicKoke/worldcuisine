
from pathlib import Path
import json

# Hoofdmap van World Cuisine
PROJECT_MAP = Path(__file__).resolve().parent

# Mappen met recepten en afbeeldingen
JSON_MAP = PROJECT_MAP / "data" / "recepten"
AFBEELDINGEN_MAP = PROJECT_MAP / "images" / "recepten"

aantal_recepten = 0
gevonden = 0
ontbrekend = []
oude_verwijzingen = []
json_fouten = []

for bestand in sorted(JSON_MAP.glob("*.json")):
    aantal_recepten += 1

    try:
        with open(bestand, encoding="utf-8") as f:
            recept = json.load(f)
    except (json.JSONDecodeError, OSError) as fout:
        json_fouten.append((bestand.name, str(fout)))
        continue

    # Zoek alle afbeeldingsverwijzingen in de JSON,
    # onafhankelijk van de gebruikte veldnaam.
    def zoek_afbeeldingen(data):
        if isinstance(data, dict):
            for waarde in data.values():
                yield from zoek_afbeeldingen(waarde)
        elif isinstance(data, list):
            for waarde in data:
                yield from zoek_afbeeldingen(waarde)
        elif isinstance(data, str):
            if data.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp")
            ):
                yield data

    for verwijzing in zoek_afbeeldingen(recept):

        # Controleer of er nog oude AI.png-verwijzingen zijn
        if verwijzing.endswith("AI.png"):
            oude_verwijzingen.append(
                (bestand.name, verwijzing)
            )

        # Controleer de WebP-afbeeldingen
        if verwijzing.lower().endswith(".webp"):

            # Een verwijzing kan een pad of alleen
            # een bestandsnaam bevatten.
            naam = Path(verwijzing).name
            afbeelding = AFBEELDINGEN_MAP / naam

            if afbeelding.is_file():
                gevonden += 1
            else:
                ontbrekend.append(
                    (bestand.name, verwijzing)
                )

print("\n========== CONTROLE WORLD CUISINE ==========")
print(f"JSON-bestanden gecontroleerd: {aantal_recepten}")
print(f"WebP-verwijzingen gevonden:    {gevonden}")
print(f"Ontbrekende WebP-bestanden:    {len(ontbrekend)}")
print(f"Oude AI.png-verwijzingen:      {len(oude_verwijzingen)}")
print(f"JSON-leesfouten:               {len(json_fouten)}")

if ontbrekend:
    print("\n--- ONTBREKENDE WEBP-AFBEELDINGEN ---")
    for recept, afbeelding in ontbrekend:
        print(f"{recept}: {afbeelding}")

if oude_verwijzingen:
    print("\n--- OUDE PNG-VERWIJZINGEN ---")
    for recept, afbeelding in oude_verwijzingen:
        print(f"{recept}: {afbeelding}")

if json_fouten:
    print("\n--- JSON-FOUTEN ---")
    for bestand, fout in json_fouten:
        print(f"{bestand}: {fout}")

if not (ontbrekend or oude_verwijzingen or json_fouten):
    print("\nAlle gecontroleerde verwijzingen zijn in orde!")

print("============================================")
