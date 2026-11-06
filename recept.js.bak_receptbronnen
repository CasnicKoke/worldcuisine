/* WorldCuisine — één herbruikbare receptpagina; inhoud komt uit JSON. */
'use strict';

const receptElement = document.getElementById('recept');
const paginaParameters = new URLSearchParams(window.location.search);
const receptSleutel = paginaParameters.get('id');
const terugRegio = paginaParameters.get('regio');
const terugUrl = terugRegio && /^[a-z0-9-]+$/i.test(terugRegio)
    ? `worldmap.html?regio=${encodeURIComponent(terugRegio)}`
    : 'worldmap.html';

document.querySelectorAll('a[href="worldmap.html"]').forEach(link => {
    link.href = terugUrl;
});

function element(naam, klasse, tekst) {
  const el = document.createElement(naam);
  if (klasse) el.className = klasse;
  if (tekst !== undefined && tekst !== null) el.textContent = String(tekst);
  return el;
}

function isAanwezig(waarde) {
  return waarde !== null && waarde !== undefined && waarde !== '';
}

function minutenTekst(minuten) {
  if (!Number.isFinite(minuten) || minuten < 0) return null;
  if (minuten < 60) return `${minuten} min`;
  const uur = Math.floor(minuten / 60);
  const rest = minuten % 60;
  return rest ? `${uur} uur ${rest} min` : `${uur} uur`;
}

function toonFout(bericht) {
  receptElement.replaceChildren(element('h1', 'error-title', 'Recept niet beschikbaar'), element('p', 'error-body', bericht));
  const a = element('a', 'back-link', '← Terug naar de wereldkaart');
  a.href = terugUrl;
  receptElement.append(a);
}

function bronVermelding(bron, type = 'recept') {
  if (!bron || !Object.values(bron).some(isAanwezig)) return null;

  const label = type === 'recept'
    ? 'Receptbron'
    : 'Aanvullende bron';

  const delen = [];

  if (isAanwezig(bron.auteur)) {
    delen.push(bron.auteur);
  }

  if (isAanwezig(bron.receptTitel)) {
    delen.push(`‘${bron.receptTitel}’`);
  }

  if (isAanwezig(bron.kookboek)) {
    delen.push(`uit ${bron.kookboek}`);
  }

  if (isAanwezig(bron.jaar)) {
    delen.push(`(${bron.jaar})`);
  }

  if (isAanwezig(bron.pagina)) {
    delen.push(`p. ${bron.pagina}`);
  }

  const tekst = delen.length
    ? `${label}: ${delen.join(', ')}.`
    : `${label}:`;

  const p = element('p', 'recipe-source', tekst);

  if (isAanwezig(bron.url) && /^https?:\/\//i.test(bron.url)) {
    const a = element('a', '', ' Bekijk bron ↗');
    a.href = bron.url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    p.append(a);
  }

  return p;
}

function toonRecept(data) {
  document.title = `${data.titel || 'Recept'} | World Cuisine`;
  receptElement.replaceChildren();

  const artikel = element('article', 'recipe-article');
  if (isAanwezig(data.afbeelding)) {
    const afbeelding = element('img', 'recipe-hero-image');
    afbeelding.src = data.afbeelding;
    afbeelding.alt = `Foto van ${data.titel || 'het gerecht'}`;
    afbeelding.decoding = 'async';
    afbeelding.addEventListener('error', () => afbeelding.remove(), {once: true});
    artikel.append(afbeelding);
  }

  const kop = element('div', 'recipe-intro');
  kop.append(element('p', 'recipe-kicker', 'PROEF DE WERELD'));
  kop.append(element('h1', 'recipe-title', data.titel || 'Onbekend recept'));
  const beschrijving = data.beschrijving || data.korteBeschrijving;
  if (isAanwezig(beschrijving)) kop.append(element('p', 'recipe-description', beschrijving));
  artikel.append(kop);

  const meta = element('div', 'recipe-meta');
  const gegevens = [
    ['Bereidingstijd', minutenTekst(data.bereidingstijdMinuten)],
    ['Porties', Number.isFinite(data.porties) && data.porties > 0 ? `${data.porties} personen` : '4 personen'],
    ['Moeilijkheid', isAanwezig(data.moeilijkheid) ? data.moeilijkheid : null]
  ];
  gegevens.forEach(([label, waarde]) => {
    if (!isAanwezig(waarde)) return;
    const blok = element('div', 'recipe-meta-item');
    const iconen = {'Bereidingstijd':'◷', 'Porties':'♟', 'Moeilijkheid':'♧'};
    blok.append(element('span', 'recipe-meta-icon', iconen[label] || '✧'));
    const tekst = element('div', 'recipe-meta-copy');
    tekst.append(element('strong', 'recipe-meta-label', label), element('span', 'recipe-meta-value', waarde));
    blok.append(tekst);
    meta.append(blok);
  });
  if (meta.children.length) artikel.append(meta);

  const kolommen = element('div', 'recipe-columns');
  const ingredientenSectie = element('section', 'recipe-section recipe-ingredients');
  ingredientenSectie.append(element('h2', '', 'Ingrediënten'));
  ingredientenSectie.append(element('p', 'recipe-serving-note', `Voor ${Number.isFinite(data.porties) && data.porties > 0 ? data.porties : 4} personen`));
  const ingredienten = Array.isArray(data.ingredienten) ? data.ingredienten : [];
  if (ingredienten.length) {
    const lijst = element('ul', 'ingredients-list');
    ingredienten.forEach(ing => {
      let tekst = '';
      if (typeof ing === 'string') tekst = ing;
      else if (ing && typeof ing === 'object') {
        tekst = [ing.hoeveelheid, ing.eenheid, ing.naam || ing.ingredient || ing.id].filter(isAanwezig).join(' ');
      }
      if (tekst) lijst.append(element('li', '', tekst));
    });
    ingredientenSectie.append(lijst);
  } else {
    ingredientenSectie.append(element('p', 'missing-data', 'De ingrediënten worden nog aangevuld.'));
  }
  kolommen.append(ingredientenSectie);

  const stappenSectie = element('section', 'recipe-section recipe-method');
  stappenSectie.append(element('h2', '', 'Bereidingswijze'));
  const stappen = Array.isArray(data.bereiding) ? data.bereiding : [];
  if (stappen.length) {
    const lijst = element('ol', 'steps-list');
    stappen.forEach(stap => {
      const tekst = typeof stap === 'string' ? stap : stap && (stap.tekst || stap.instructie);
      if (tekst) lijst.append(element('li', '', tekst));
    });
    stappenSectie.append(lijst);
  } else {
    stappenSectie.append(element('p', 'missing-data', 'De bereidingsstappen worden nog aangevuld.'));
  }
  kolommen.append(stappenSectie);
  artikel.append(kolommen);

  // Historisch weetje, alleen voor recepten die dit veld hebben.
  if (isAanwezig(data.weetje)) {
    const kader = element('aside', 'recipe-history-note');
    kader.append(element('h2', '', 'Wist je dat?'));
    kader.append(element('p', '', data.weetje));
    artikel.append(kader);
  }
  
  const bron = bronVermelding(data.bron, 'recept');
  if (bron) artikel.append(bron);
  // Aanvullende bronnen, naast de bestaande hoofdbron.
  if (Array.isArray(data.extraBronnen)) {
    data.extraBronnen.forEach(bronData => {
      const extra = bronVermelding(bronData, 'aanvullend');
      if (extra) {
        extra.classList.add('recipe-source-extra');
        artikel.append(extra);
      }
    });
  }
  receptElement.append(artikel);
}

async function start() {
  if (!receptSleutel || !/^[a-z0-9][a-z0-9_-]*$/i.test(receptSleutel)) {
    toonFout('Er is geen geldig recept geselecteerd.');
    return;
  }
  try {
    const response = await fetch(`data/recepten/${encodeURIComponent(receptSleutel)}.json`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (data.sleutel !== receptSleutel) throw new Error('Recept-ID komt niet overeen.');
    toonRecept(data);
  } catch (fout) {
    console.error('WorldCuisine: recept laden mislukt:', fout);
    toonFout('Controleer of het receptbestand bestaat en of je de website via Live Server opent.');
  }
}

start();
