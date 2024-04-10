import eel
import jsonpickle
from supabase import create_client, Client

SUPABASE_URL = "https://cjxferfvtfodvzonnqyk.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqeGZlcmZ2dGZvZHZ6b25ucXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTEzNzI0MDQsImV4cCI6MjAyNjk0ODQwNH0.Yo_cwzRX5y_wQH08aQ57NnKw_KXgHajvfQ1Qk_Q6y_Q"

supabase = create_client(SUPABASE_URL, API_KEY)
eel.init('static')

class User:
    def __init__(self, user, passwd):
        self.supabase_obj = None
        self.datab_usr = None

        self.user = user
        self.passwd = passwd
    def login(self):
        try:
            data = supabase.auth.sign_in_with_password({"email": self.user, "password": self.passwd})
            self.supabase_obj = data
            self.datab_usr = self.get_database_user()

            eel.redirect('app.html')
        except Exception as e:
            eel.login_error(str(e))
    def register(self):
        try:
            print(self.user, self.passwd)
            supabase.auth.sign_up({"email": self.user, "password": self.passwd})
            eel.signup_success()
        except Exception as e:
            eel.signup_error(str(e))
    def __str__(self):
        if self.supabase_obj is None:
            return None
        data = {
            'id' : self.supabase_obj.user.id,
            'email' : self.supabase_obj.user.email,
            'username' : self.datab_usr['username'],
            'avatar_url' : self.datab_usr['avatar_url'] if 'avatar_url' in self.datab_usr else '',
        }
        return jsonpickle.encode(data)
    def get_database_user(self):
        if self.supabase_obj is None:
            return None
        profile = supabase.table('profiles').select("*").eq('id', self.supabase_obj.user.id).execute()

        if len(profile.data) == 0:
            supabase.table('profiles').insert([{
                'id' : self.supabase_obj.user.id,
                'username' : self.supabase_obj.user.email.split('@')[0],
            }]).execute()

            profile = supabase.table('profiles').select("*").eq('id', self.supabase_obj.user.id).execute()

        return profile.data[0]
    def update(self, data):
        print('-----UPDATE-----')
        print(data)

        if self.supabase_obj is None:
            return None
        
        try :
            supabase.table('profiles').update(data).eq('id', self.supabase_obj.user.id).execute()

            self.datab_usr = self.get_database_user()
        except Exception as e:
            eel.send_error(str(e))

currentUser = None

@eel.expose
def login_user(user, passwd):
    global currentUser
    currentUser = User(user, passwd)
    currentUser.login()

@eel.expose
def register_user(user, passwd):
    global currentUser
    currentUser = User(user, passwd)
    currentUser.register()

@eel.expose
def get_user():
    global currentUser
    eel.set_user(str(currentUser))

@eel.expose
def change_username(new_username):
    global currentUser
    currentUser.update({'username': new_username})

eel.start('login.html', cmdline_args=['--disable-lcd-text'], size=(950, 750), position=(20, 20))