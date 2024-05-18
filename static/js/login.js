/*
login.js
-----------------------
Sert au fonctionnement de la page de connexion et d'inscription
*/

// permet de demander à Python de se connecter
function loginUser() {
    // récupère les valeurs des champs email et password
    var email = document.getElementById("login-email").value;
    var password = document.getElementById("login-password").value;

    mount('loading', true);
    eel.login_user(email, password);
}

// permet de demander à Python de s'inscrire
function signupUser() {
    // récupère les valeurs des champs email, password et password2
    var email = document.getElementById("signup-email").value;
    var password = document.getElementById("signup-password").value;
    var password2 = document.getElementById("signup-password-confirm").value;

    // vérifie que les champs ne sont pas vides
    if (email.trim() == "" || password.trim() == "" || password2.trim() == "") {
        mount('signupError', "Merci de remplir tous les champs.");
        return;
    }

    // vérifie que les mots de passe correspondent
    if (password != password2) {
        mount('signupError', "Les mots de passe ne correspondent pas.");
        return;
    }

    // affiche l'icône de chargement
    mount('loading', true);

    // demande à Python de s'inscrire
    eel.register_user(email, password);
}

// (utilisée par Python) en cas d'erreur lors de la connexion
function login_error(text) {
    // affiche l'erreur
    mount('loginError', 'Erreur inconnue (' + text + ')');
    mount('loading', false);

    if (text.trim() == 'Invalid login credentials') {
        mount('loginError', "Identifiants incorrects.");
    }

    if (text.trim() == 'You must provide either an email or phone number and a password') {
        mount('loginError', "Vous devez fournir un email ou un numéro de téléphone et un mot de passe.");
    }
}


// (utilisée par Python) en cas d'erreur lors de l'inscription
function signup_error(text) {
    mount('signupError', text);
    mount('loading', false);
}


// (utilisée par Python) en cas d'inscription réussie
function signup_success() {
    mount('signupSuccess', true);
    mount('signupError', null);
    mount('loading', false);
}

// Exposer les fonctions aux scripts Python
eel.expose(login_error);
eel.expose(signup_error);
eel.expose(signup_success);