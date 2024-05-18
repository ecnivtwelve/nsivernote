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

function set_loading_state(is_loading) {
    // body.__x.$data.is_loading = is_loading;
    mount('is_loading', is_loading);
}
eel.expose(set_loading_state);

function set_tasks(data) {
    console.log(JSON.parse(data));
    tasks = JSON.parse(data);

    console.log(tasks);

    // body.__x.$data.tasks = tasks;
    mount('tasks', tasks);
    mount('tasks_loaded', true);
}
eel.expose(set_tasks);

function create_new_list(name) {
    eel.create_new_list(name);
}

function rename_list(id, new_name) {
    eel.rename_list(id, new_name);
}

function delete_list(id) {
    eel.delete_list(id);
}

function update_list_json(id, json_tasks) {
    eel.update_tasks(id, json_tasks);
}

eel.get_user();
eel.get_tasks();