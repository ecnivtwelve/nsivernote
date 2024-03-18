import eel
import lxml
import json
import pronotepy
from pronotepy.ent import ac_rennes

eel.init('static')

client = None

@eel.expose
def login_ttc(user, passwd, url):
    try :
        if(("toutatice.fr" in url) and ("login=true" not in url)):
            client = pronotepy.Client(url,
                    username=user,
                    password=passwd,
                    ent=ac_rennes)
        else:
            client = pronotepy.Client(url,
                    username=user,
                    password=passwd)
        if client.logged_in:
            info = client.info
            data = {
                "logged_in": True,
                "name": info.name,
                "establishment": info.establishment,
                "class_name": info.class_name,
                "ine_number": info.ine_number,
                "phone": info.phone,
                "email": info.email,
                "address": info.address,
                "profile_picture": info.profile_picture.url if info.profile_picture else None,
            }
            eel.ret_user_data(data)
        else:
            eel.ret_user_data({"logged_in": False, "error": "Login failed"})
    except Exception as e:
        eel.ret_user_data({"logged_in": False, "error": str(e)})
    

eel.start('app.html', mode='edge')