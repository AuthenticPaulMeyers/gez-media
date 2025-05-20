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

def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/static', instance_relative_config=True)

    # create and configure the app
    # Load environment variables from .env file
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
    else:
        # Load the test configuration if provided
        app.config.from_mapping(test_config)

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







    return app