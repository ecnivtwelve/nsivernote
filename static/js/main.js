function get_user() {
    eel.get_user();
}

function set_user(data) {
    console.log(JSON.parse(data));
    user = JSON.parse(data);
}
eel.expose(set_user);

get_user();