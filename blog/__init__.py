from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#initialize the SQLAlchemy object for database management
db = SQLAlchemy()
#set the name of the database to be used
DB_NAME = "blog.db"

#define the main factory function for creating the Flask app
def create_app():
    #create a new Flask app instance
    app = Flask(__name__)
    #set the secret key for the app
    app.config['SECRET_KEY'] = "blog"
    #set the URI of the SQLAlchemy database to be used by the app
    app.config['SQL_ALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #initialize the SQLAlchemy object 
    db.init_app(app)

    #import the views and auth blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    
    from .models import User

    #create the database for the app
    create_database(app)

  
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    #initialize the LoginManager
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    #return the Flask app instance
    return app

# function for creating the database for the app
def create_database(app):
    #check if the database file exists
    if not path.exists("website/" + DB_NAME):
        #create the database tables if the file does not exist
        db.create_all(app=app)
        print("Created database!")
