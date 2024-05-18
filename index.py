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

class TaskList:
    def __init__(self):
        """
        Crée un objet TaskList.
        Sauvegarde les tâches de l'utilisateur dans self.tasks.
        """
        # Variables de données
        self.id = ''
        self.title = ''
        self.description = ''
        self.tasks = ''
        self.identifier = ''
        self.share = False
        self.creator = ''

    def get_tasks(self, req_id):
        """
        Récupère les tâches de l'utilisateur dans la base de données.
        """
        if self.id == '':
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (SELECT * FROM tasks WHERE id = self.id)
        tasks = supabase.table('tasks').select("*").eq('id', req_id).execute()
        # Retourne les tâches de l'utilisateur

        self.id = tasks.data[0]['id']
        self.title = tasks.data[0]['title']
        self.description = tasks.data[0]['description']
        self.tasks = tasks.data[0]['tasks']
        self.identifier = tasks.data[0]['identifier']
        self.share = tasks.data[0]['share']
        self.creator = tasks.data[0]['creator']

    def __str__(self):
        """
        Retourne les données de l'utilisateur sous forme de JSON.
        """
        if self.id == '':
            # Si l'utilisateur n'est pas connecté
            return None
        # Formatage des données de l'utilisateur en JSON
        data = {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'tasks' : self.tasks,
            'identifier' : self.identifier,
            'share' : self.share,
            'creator' : self.creator,
        }
        # Retourne les données sous forme de JSON
        return jsonpickle.encode(data)

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

    def get_tasks(self):
        """
        Récupère les tâches de l'utilisateur dans la base de données.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (SELECT * FROM tasks WHERE creator = self.supabase_obj.user.id)
        tasks = supabase.table('tasks').select("*").eq('creator', self.supabase_obj.user.id).execute()

        print(self.supabase_obj.user.id)
        print(tasks)

        # Retourne les tâches de l'utilisateur
        return tasks.data

    def new_task(self, name):
        """
        Crée une nouvelle tâche pour l'utilisateur.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (INSERT INTO tasks VALUES (self.supabase_obj.user.id, name))
        supabase.table('tasks').insert([{
            'creator' : self.supabase_obj.user.id,
            'name' : name,
        }]).execute()

    def rename_task(self, id, new_name):
        """
        Renomme une tâche de l'utilisateur.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (UPDATE tasks SET name = new_name WHERE id = id)
        supabase.table('tasks').update({'name': new_name}).eq('id', id).execute()

    def delete_task(self, id):
        """
        Supprime une tâche de l'utilisateur.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (DELETE FROM tasks WHERE id = id)
        supabase.table('tasks').delete().eq('id', id).execute()

    def update_tasks(self, id, json_tasks):
        """
        Met à jour les tâches de l'utilisateur.
        """
        if self.supabase_obj is None:
            # Si l'utilisateur n'est pas connecté
            return None
        # Requête base de données (UPDATE tasks SET json = json_tasks WHERE id = id)
        supabase.table('tasks').update({'json': json_tasks}).eq('id', id).execute()

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
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Retourne les données de l'utilisateur actuel
    eel.set_user(str(currentUser))
    # Fin de chargement
    eel.set_loading_state(False)

@eel.expose
def change_username(new_username):
    """
    (JS) Change le nom d'utilisateur de l'utilisateur actuel.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Met à jour le nom d'utilisateur
    currentUser.update({'username': new_username})
    # Fin de chargement
    eel.set_loading_state(False)

@eel.expose
def get_tasks():
    """
    (JS) Récupère les tâches de l'utilisateur actuel.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Retourne les tâches de l'utilisateur actuel
    tasks = currentUser.get_tasks()
    # Envoie les tâches à l'interface
    eel.set_tasks(jsonpickle.encode(tasks))
    # Fin de chargement
    eel.set_loading_state(False)

@eel.expose
def get_task_list(req_id):
    """
    (JS) Récupère les tâches de l'utilisateur actuel.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Retourne les tâches de l'utilisateur actuel
    tasks = TaskList()
    tasks.get_tasks(req_id)
    eel.set_task_list(str(tasks))

@eel.expose
def create_new_list(title):
    """
    (JS) Crée une nouvelle liste de tâches.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Crée une nouvelle liste de tâches
    currentUser.new_task(title)
    # Met à jour les tâches de l'utilisateur actuel
    get_tasks()

@eel.expose
def rename_list(id, new_name):
    """
    (JS) Renomme une liste de tâches.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Renomme une liste de tâches
    currentUser.rename_task(id, new_name)
    # Met à jour les tâches de l'utilisateur actuel
    get_tasks()

@eel.expose
def delete_list(id):
    """
    (JS) Supprime une liste de tâches.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Supprime une liste de tâches
    currentUser.delete_task(id)
    # Met à jour les tâches de l'utilisateur actuel
    get_tasks()

@eel.expose
def update_tasks(id, json_tasks):
    """
    (JS) Met à jour les tâches de l'utilisateur actuel.
    """
    # Utilisation de la variable globale currentUser
    global currentUser
    # Affiche le chargement sur l'interface
    eel.set_loading_state(True)
    # Enregistre les nouvelles tâches
    currentUser.update_tasks(id, json_tasks)
    # Met à jour les tâches de l'utilisateur actuel
    get_tasks()

# Lancement de l'application avec Eel
eel.start('login.html', cmdline_args=['--disable-lcd-text'], size=(950, 680), position=(20, 20))