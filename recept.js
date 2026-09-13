const params =
    new URLSearchParams(window.location.search);

const receptId =
    params.get("id");
    console.log(receptId);

const recept =
    recepten[receptId];
    console.log(recept);

document.getElementById("recept").innerHTML = `
    <h1>${recept.titel}</h1>

    <img src="${recept.afbeelding}" alt="${eschrijving}</p>

    <h2>Ingrediënten</h2>

    <ul>
        ${recept.ingredienten
            .map(i => `<li>${i}</li>`)
            .join("")}
    </ul>

    <h2>Bereiding</h2>

    <ol>
        ${recept.bereiding
            .map(stap => `<li>${stap}</li>`)
            .join("")}
    </ol>
`;