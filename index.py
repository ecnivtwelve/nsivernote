import eel
import jsonpickle
from supabase import create_client, Client

SUPABASE_URL = "https://cjxferfvtfodvzonnqyk.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqeGZlcmZ2dGZvZHZ6b25ucXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTEzNzI0MDQsImV4cCI6MjAyNjk0ODQwNH0.Yo_cwzRX5y_wQH08aQ57NnKw_KXgHajvfQ1Qk_Q6y_Q"

supabase = create_client(SUPABASE_URL, API_KEY)
eel.init('static')

@eel.expose
def login_user(user, passwd):
    try:
        data = supabase.auth.sign_in_with_password({"email": user, "password": passwd})
        print(data)
        eel.python_console('User logged in successfully!')
        eel.redirect('app.html')
        eel.python_console(jsonpickle.encode(data))
    except Exception as e:
        eel.python_console(str(e))

@eel.expose
def register_user(user, passwd):
    try:
        data = supabase.auth.sign_up({"email": user, "password": passwd})
        eel.python_console('User registered successfully!')
    except Exception as e:
        eel.python_console(str(e))

@eel.expose
def get_user():
    try :
        print('Getting user...')
        user = supabase.auth.get_user()
        eel.set_user(jsonpickle.encode(user))
    except Exception as e:
        eel.redirect('login.html')
    

eel.start('login.html', mode='edge')