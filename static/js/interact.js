function set_element_text(id, text) {
    let element = document.getElementById(id);
    element.innerHTML = text;
}

function set_element_value(id, value) {
    let element = document.getElementById(id);
    element.value = value;
}

function redirect(url) {
    window.location.href = url;
}

const mount = (name, data) => {
    const e = new CustomEvent('mounted', { detail: { name, data } });
    document.body.dispatchEvent(e);
};

function send_error(text) {
    mount('error', text);
    console.error('[EEL_Nsivernote] : ', text);
}

eel.expose(set_element_text);
eel.expose(set_element_value);
eel.expose(redirect);