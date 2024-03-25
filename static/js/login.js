function loginUser() {
    var email = document.getElementById("login-email").value;
    var password = document.getElementById("login-password").value;

    eel.login_user(email, password);
}

function signupUser() {
    var email = document.getElementById("signup-email").value;
    var password = document.getElementById("signup-password").value;
    var password2 = document.getElementById("signup-password-confirm").value;

    if (email.trim() == "" || password.trim() == "" || password2.trim() == "") {
        alert("Please fill in all fields.");
        return;
    }

    if (password != password2) {
        alert("Passwords do not match.");
        return;
    }

    eel.register_user(email, password);
}

function python_console(text) {
    let login_console = document.getElementById("python-login");
    let signup_console = document.getElementById("python-signup");

    // add text to a new line in both textareas
    login_console.value += text + "\n";
    signup_console.value += text + "\n";

    // scroll to the bottom
    login_console.scrollTop = login_console.scrollHeight;
    signup_console.scrollTop = signup_console.scrollHeight;
}

eel.expose(python_console);