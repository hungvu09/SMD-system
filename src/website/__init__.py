from urllib import response
from flask import Flask
from flask_login import LoginManager
import os
from _object.entities.model_users import User


from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjhjhjhj'
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')
#Init - login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        
        user = User.get(user_id)
        return user
    
#ket noi supabase va debug ket noi
    from data.supa import supabase
    #print("Supabase connected:", supabase is not None)

    from .auth import auth
    from .views import views

#import cac cau truc du lieu tu model
    

    #dang ky blueprint
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')


    return app