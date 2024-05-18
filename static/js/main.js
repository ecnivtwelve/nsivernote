/*
main.js
-----------------------
Sert au fonctionnement de la page principale de l'application (après connexion)
*/

// définit la variable user, qui contiendra les informations de l'utilisateur
let user = {};

// permet de changer le nom d'utilisateur
function change_username(name) {
    console.log('js_chg_nm', name);
    eel.change_username(name);
}

// (utilisée par Python) mettre à jour les informations de l'utilisateur
function set_user(data) {
    console.log(JSON.parse(data));
    user = JSON.parse(data);

    // body.__x.$data.user = user;
    mount('user', user);
    mount('user_loaded', true);
}
eel.expose(set_user);

// (utilisée par Python) mettre à jour l'état de chargement
function set_loading_state(is_loading) {
    // body.__x.$data.is_loading = is_loading;
    mount('is_loading', is_loading);
}
eel.expose(set_loading_state);

// (utilisée par Python) mettre à jour les tâches
function set_tasks(data) {
    console.log(JSON.parse(data));
    tasks = JSON.parse(data);

    console.log(tasks);

    // body.__x.$data.tasks = tasks;
    mount('tasks', tasks);
    mount('tasks_loaded', true);
}
eel.expose(set_tasks);

// (utilisée par Python) créer une nouvelle tâche
function create_new_list(name) {
    eel.create_new_list(name);
}

// (utilisée par Python) renommer une tâche
function rename_list(id, new_name) {
    eel.rename_list(id, new_name);
}

// (utilisée par Python) supprimer une tâche
function delete_list(id) {
    eel.delete_list(id);
}

// (utilisée par Python) remplacer les données JSON de la tâche
function update_list_json(id, json_tasks) {
    eel.update_tasks(id, json_tasks);
}

// demande a Python les informations de l'utilisateur
eel.get_user();
// demande a Python les tâches
eel.get_tasks();