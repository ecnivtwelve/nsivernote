const base_url = 'https://0350053t.pronote.toutatice.fr/pronote/eleve.html';

document.getElementById('url').value = base_url;

eel.expose(ret_user_data); // Expose this function to Python
function ret_user_data(x) {
    document.getElementById('userdata').innerHTML = JSON.stringify(x, null, 4);
    console.log(x);

    if (x['logged_in'] == true) {
        document.getElementById('err').style.display = 'none';
        // show data in HTML
        document.getElementById('userprofile-name').innerText = x['name'];
        document.getElementById('userprofile-class-name').innerText = x['class_name'];
        document.getElementById('userprofile-establishment').innerText = x['establishment'];
        document.getElementById('userprofile-email').innerText = x['email'];
        document.getElementById('userprofile-pdp').src = x['profile_picture'];
    }
    else {
        document.getElementById('err').style.display = 'block';
        document.getElementById('err').innerText = x['error'];
    }
}

function login() {
    let usr = document.getElementById('user').value;
    let pass = document.getElementById('pass').value;
    let url = document.getElementById('url').value;
    eel.login_ttc(usr, pass, url);
};

let subButton = document.getElementById('sub');
subButton.addEventListener('click', login);