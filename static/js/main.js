let user = {};

function change_username(name) {
    console.log('js_chg_nm', name);
    eel.change_username(name);
}

function set_user(data) {
    console.log(JSON.parse(data));
    user = JSON.parse(data);

    // body.__x.$data.user = user;
    mount('user', user);
    mount('user_loaded', true);
}
eel.expose(set_user);

function set_tasks(data) {
    console.log(JSON.parse(data));
    tasks = JSON.parse(data);

    console.log(tasks);

    // body.__x.$data.tasks = tasks;
    mount('tasks', tasks);
    mount('tasks_loaded', true);
}
eel.expose(set_tasks);

eel.get_user();
eel.get_tasks();