#!/usr/bin/env python3
"""Voegt optioneel historisch weetje en extra bronnen toe aan WorldCuisine."""
from pathlib import Path
p = Path('recept.js')
if not p.exists():
    raise SystemExit('Voer dit script uit vanuit de hoofdmap van WorldCuisine.')
s = p.read_text(encoding='utf-8')
marker = '  const bron = bronVermelding(data.bron);'
tail = '  if (bron) artikel.append(bron);'
if 'recipe-history-note' not in s:
    if s.count(marker) != 1 or s.count(tail) != 1:
        raise SystemExit('recept.js wijkt af: invoegpunten niet gevonden. Niets gewijzigd.')
    new = '''  // Historisch weetje, alleen voor recepten die dit veld hebben.
  if (isAanwezig(data.weetje)) {
    const kader = element('aside', 'recipe-history-note');
    kader.append(element('h2', '', 'Wist je dat?'));
    kader.append(element('p', '', data.weetje));
    artikel.append(kader);
  }
'''
    sources = '''  // Aanvullende bronnen, naast de bestaande hoofdbron.
  if (Array.isArray(data.extraBronnen)) {
    data.extraBronnen.forEach(bronData => {
      const extra = bronVermelding(bronData);
      if (extra) {
        extra.classList.add('recipe-source-extra');
        artikel.append(extra);
      }
    });
  }
'''
    s=s.replace(marker,new+marker).replace(tail,tail+'\n'+sources.rstrip())
    Path('recept.js.bak').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
    p.write_text(s,encoding='utf-8')
    print('recept.js bijgewerkt; backup: recept.js.bak')
else:
    print('recept.js bevat al ondersteuning voor historisch weetje.')
css = Path('recept-detail.css')
if css.exists():
    c=css.read_text(encoding='utf-8')
    if '.recipe-history-note {' not in c:
        extension = '''
/* Historisch weetje bij een recept */
.recipe-history-note {
    margin: 24px 0 16px;
    padding: 18px 22px;
    border-top: 1px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    background: rgba(255, 246, 225, 0.28);
}

.recipe-history-note h2 {
    margin: 0 0 10px;
    font-size: 1.35rem;
}

.recipe-history-note p {
    margin: 0;
    line-height: 1.6;
}

.recipe-source-extra {
    margin-top: 7px;
    padding-top: 7px;
    border-top: none;
}
'''
        Path('recept-detail.css.bak').write_text(c,encoding='utf-8')
        css.write_text(c+extension,encoding='utf-8')
        print('recept-detail.css uitgebreid; backup: recept-detail.css.bak')
