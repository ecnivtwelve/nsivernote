/*
interact.js
-----------------------
Sert a Python pour pouvoir interagir avec le DOM de la page web
*/

// (utilisée par Python) mettre à jour le texte d'un élément
function set_element_text(id, text) {
    let element = document.getElementById(id);
    element.innerHTML = text;
}

// (utilisée par Python) mettre à jour la valeur d'un élément
function set_element_value(id, value) {
    let element = document.getElementById(id);
    element.value = value;
}

// (utilisée par Python) rediriger l'utilisateur
function redirect(url) {
    window.location.href = url;
}

// permet d'envoyer une donnée à l'interface graphique
const mount = (name, data) => {
    const e = new CustomEvent('mounted', { detail: { name, data } });
    document.body.dispatchEvent(e);
};

// (utilisée par Python) en cas d'erreur
function send_error(text) {
    mount('error', text);
    console.error('[EEL_Nsivernote] : ', text);
}

// Expose les fonctions au code Python
eel.expose(set_element_text);
eel.expose(set_element_value);
eel.expose(redirect);