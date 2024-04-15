import eel
import jsonpickle
from supabase import create_client, Client

# Variables de connexion à la base de données à distance Supabase (devrait pas être exposé dans le code, mais pour les besoins d'un petit projet, on le laisse ici)
SUPABASE_URL = "https://cjxferfvtfodvzonnqyk.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqeGZlcmZ2dGZvZHZ6b25ucXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTEzNzI0MDQsImV4cCI6MjAyNjk0ODQwNH0.Yo_cwzRX5y_wQH08aQ57NnKw_KXgHajvfQ1Qk_Q6y_Q"

# Connexion à la base de données Supabase
supabase = create_client(SUPABASE_URL, API_KEY)
# Initialisation de Eel
eel.init('static')

class User:
    def __init__(self, user, passwd):
        """
        Crée un objet User.
        Sauvegarde les identifiants pour se connecter via login() ou créer un compte avec via register().

        IN :
            user (str) : email de l'utilisateur
            passwd (str) : mot de passe de l'utilisateur
        """

        # Variables de données
        self.supabase_obj = None
        self.datab_usr = None

        # Identifiants
        self.user = user
        self.passwd = passwd

    def login(self):
        """
        Connecte l'utilisateur avec les identifiants donnés lors de l'initialisation de l'objet.
        -> Sauvegarde les données de l'utilisateur dans self.supabase_obj et self.datab_usr
        """
        try:
            # Connexion à la base de données
            data = supabase.auth.sign_in_with_password({"email": self.user, "password": self.passwd})
            # Sauvegarde des données de l'utilisateur
            self.supabase_obj = data
            self.datab_usr = self.get_database_user()

            # Redirection vers l'application
            eel.redirect('app.html')
        except Exception as e:
            # En cas d'erreur, renvoie un message d'erreur
            eel.login_error(str(e))

    def register(self):
        """
        Crée un compte utilisateur avec les identifiants donnés lors de l'initialisation de l'objet.
        -> Sauvegarde les données de l'utilisateur dans self.supabase_obj et self.datab_usr
        """
        try:
            # Création sur la base de données
            supabase.auth.sign_up({"email": self.user, "password": self.passwd})
            # Renvoie un message de succès si tout s'est bien passé
            eel.signup_success()
        except Exception as e:
            # En cas d'erreur, renvoie un message d'erreur
            eel.signup_error(str(e))

    def __str__(self):
        """
        Retourne les données de l'utilisateur sous forme de JSON.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Formatage des données de l'utilisateur en JSON
        data = {
            'id' : self.supabase_obj.user.id,
            'email' : self.supabase_obj.user.email,
            'username' : self.datab_usr['username'],
            'avatar_url' : self.datab_usr['avatar_url'] if 'avatar_url' in self.datab_usr else '',
        }
        # Retourne les données sous forme de JSON
        return jsonpickle.encode(data)

    def get_database_user(self):
        """
        Récupère les données de l'utilisateur dans la base de données.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (SELECT * FROM profiles WHERE id = self.supabase_obj.user.id)
        profile = supabase.table('profiles').select("*").eq('id', self.supabase_obj.user.id).execute()

        if len(profile.data) == 0:
            # Si l'utilisateur n'existe pas dans la base de données, on l'ajoute
            # Requête base de données (INSERT INTO profiles VALUES (self.supabase_obj.user.id, self.supabase_obj.user.email.split('@')[0]))
            supabase.table('profiles').insert([{
                'id' : self.supabase_obj.user.id,
                'username' : self.supabase_obj.user.email.split('@')[0],
            }]).execute()

            # On récupère les données de l'utilisateur
            # Requête base de données (SELECT * FROM profiles WHERE id = self.supabase_obj.user.id)
            profile = supabase.table('profiles').select("*").eq('id', self.supabase_obj.user.id).execute()

        # Retourne les données de l'utilisateur (1er élément de la liste de données)
        return profile.data[0]

    def update(self, data):
        """
        Met à jour les données de l'utilisateur dans la base de données.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        
        try :
            # Requête base de données (UPDATE profiles SET data WHERE id = self.supabase_obj.user.id)
            supabase.table('profiles').update(data).eq('id', self.supabase_obj.user.id).execute()

            # On récupère les nouvelles données de l'utilisateur
            self.datab_usr = self.get_database_user()
        except Exception as e:
            # En cas d'erreur, renvoie un message d'erreur
            eel.send_error(str(e))

# Variable de l'utilisateur actuel connecté (objet User)
currentUser = None

@eel.expose
def login_user(user, passwd):
    """
    (JS) Connecte l'utilisateur avec les identifiants donnés depuis JavaScript.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Création d'un objet User avec les identifiants donnés
    currentUser = User(user, passwd)
    # Connexion de l'utilisateur
    currentUser.login()

@eel.expose
def register_user(user, passwd):
    """
    (JS) Crée un compte utilisateur avec les identifiants donnés depuis JavaScript.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Création d'un objet User avec les identifiants donnés
    currentUser = User(user, passwd)
    # Création du compte utilisateur
    currentUser.register()

@eel.expose
def get_user():
    """
    (JS) Retourne les données de l'utilisateur actuel.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Retourne les données de l'utilisateur actuel
    eel.set_user(str(currentUser))

@eel.expose
def change_username(new_username):
    """
    (JS) Change le nom d'utilisateur de l'utilisateur actuel.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Met à jour le nom d'utilisateur
    currentUser.update({'username': new_username})

# Lancement de l'application avec Eel
eel.start('login.html', cmdline_args=['--disable-lcd-text'], size=(950, 680), position=(20, 20))