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

eel.expose(set_element_text);
eel.expose(set_element_value);
eel.expose(redirect);