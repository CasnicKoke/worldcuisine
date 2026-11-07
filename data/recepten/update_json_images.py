from pathlib import Path

# Pas dit pad aan als je JSON-bestanden ergens anders staan
JSON_MAP = Path(__file__).resolve().parent

aangepast = 0
bestanden = 0

for json_bestand in sorted(JSON_MAP.glob("*.json")):
    inhoud = json_bestand.read_text(encoding="utf-8")

    nieuwe_inhoud = inhoud.replace("AI.png", "AI.webp")

    if nieuwe_inhoud != inhoud:
        json_bestand.write_text(nieuwe_inhoud, encoding="utf-8")
        aangepast += 1
        print(f"Aangepast: {json_bestand.name}")
    bestanden += 1

print("\n--- RESULTAAT ---")
print(f"Gecontroleerde JSON-bestanden: {bestanden}")
print(f"Aangepaste JSON-bestanden:     {aangepast}")