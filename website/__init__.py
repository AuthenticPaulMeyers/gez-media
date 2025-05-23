from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_cors import CORS
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
# Initialize the CSRF protection    

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, static_url_path='/static')

    # create and configure the app
    app.config['SECRET_KEY'] = 'yugdugvucdiurhuheirhiuhiuhe37843gjbjhsdfBHHShVDHsD'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)
    csrf.init_app(app)
    CORS(app)
    # Initialize the login manager
    login_manager.init_app(app)

    from website.models import User  # Make sure you have a User model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Register the blueprints
    from website.views import views
    from website.auth import auth
    app.register_blueprint(views)
    app.register_blueprint(auth)

    # Create the database tables
    with app.app_context():
        db.create_all()


    return app