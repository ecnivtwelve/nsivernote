function loginUser() {
    var email = document.getElementById("login-email").value;
    var password = document.getElementById("login-password").value;

    mount('loading', true);
    eel.login_user(email, password);
}

function signupUser() {
    var email = document.getElementById("signup-email").value;
    var password = document.getElementById("signup-password").value;
    var password2 = document.getElementById("signup-password-confirm").value;

    if (email.trim() == "" || password.trim() == "" || password2.trim() == "") {
        mount('signupError', "Merci de remplir tous les champs.");
        return;
    }

    if (password != password2) {
        mount('signupError', "Les mots de passe ne correspondent pas.");
        return;
    }

    mount('loading', true);

    eel.register_user(email, password);
}

function login_error(text) {
    mount('loginError', text);
    mount('loading', false);

    if (text.trim() == 'Invalid login credentials') {
        mount('loginError', "Identifiants incorrects.");
    }
}

function signup_error(text) {
    mount('signupError', text);
    mount('loading', false);
}

function signup_success() {
    mount('signupSuccess', true);
    mount('signupError', null);
    mount('loading', false);
}

eel.expose(login_error);
eel.expose(signup_error);
eel.expose(signup_success);