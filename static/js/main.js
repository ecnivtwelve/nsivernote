function get_user() {
    eel.get_user();
}

function set_user(data) {
    console.log(JSON.parse(data));
    user = JSON.parse(data);

    // body.__x.$data.user = user;
    mount('user', user);
}
eel.expose(set_user);

get_user();