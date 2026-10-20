/* WorldCuisine — recepten en regio-koppelingen laden uit JSON.
   Scriptvolgorde in HTML blijft: recepten.js, daarna worldmap.js. */
let recepten = {};
let regioRecepten = {};

async function leesJSON(pad) {
    const response = await fetch(pad);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${pad}`);
    }
    return response.json();
}

const receptenGereed = Promise.all([
    leesJSON('data/recepten/index.json'),
    leesJSON('data/regio-recepten.json')
]).then(([index, regioData]) => {
    recepten = index.recepten;
    regioRecepten = regioData;
}).catch(fout => {
    console.error('Receptgegevens konden niet worden geladen:', fout);
    const container = document.getElementById('receptenContainer');
    if (container) {
        container.textContent = 'Recepten konden niet worden geladen.';
        container.style.display = 'block';
    }
    throw fout;
});
