#!/usr/bin/env python3
"""World Cuisine: ondersteunt receptBronnen naast bron en extraBronnen.
Plaats in de projectroot en voer uit: python3 update_receptbronnen.py
Maakt een backup recept.js.bak_receptbronnen.
"""
from pathlib import Path
import re
import shutil

path = Path(__file__).resolve().parent / 'recept.js'
if not path.is_file():
    raise SystemExit('Geen recept.js gevonden. Plaats dit script naast recept.js in de projectmap.')
src = path.read_text(encoding='utf-8')
if 'const receptBronnen = Array.isArray(data.receptBronnen)' in src:
    print('recept.js ondersteunt receptBronnen al; niets gewijzigd.')
    raise SystemExit(0)

# Target only the original source-rendering region, not the rest of the website.
start = src.find('  const bron = bronVermelding(data.bron')
end = src.find('  receptElement.append(artikel);', start)
if start < 0 or end < 0:
    raise SystemExit('Bronweergave niet herkend. recept.js is niet aangepast.')
old = src[start:end]
if 'data.extraBronnen' not in old or 'artikel.append(bron)' not in old:
    raise SystemExit('Onverwachte bronstructuur. recept.js is niet aangepast.')

# Newer recept.js already uses bronVermelding(bron,type), while older copies
# only accept bron. Keep compatibility with both signatures.
new = '''  // Receptbronnen: nieuw formaat krijgt voorrang; oude recepten blijven werken.
  const receptBronnen = Array.isArray(data.receptBronnen) && data.receptBronnen.length
    ? data.receptBronnen
    : (data.bron ? [data.bron] : []);
  receptBronnen.forEach(bronData => {
    const bron = bronVermelding(bronData, 'recept');
    if (bron) artikel.append(bron);
  });

  // Historische en andere aanvullende bronnen apart weergeven.
  if (Array.isArray(data.extraBronnen)) {
    data.extraBronnen.forEach(bronData => {
      const extra = bronVermelding(bronData, 'aanvullend');
      if (extra) {
        extra.classList.add('recipe-source-extra');
        artikel.append(extra);
      }
    });
  }
'''
updated = src[:start] + new + src[end:]
backup = path.with_name('recept.js.bak_receptbronnen')
if backup.exists():
    raise SystemExit(f'Backup bestaat al: {backup}. Hernoem/verwijder deze eerst om overschrijven te voorkomen.')
shutil.copy2(path, backup)
path.write_text(updated, encoding='utf-8')
print(f'Bijgewerkt: {path.name}; backup: {backup.name}')
