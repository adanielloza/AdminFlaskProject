# app.py
from flask import Flask
from flask_login import LoginManager
from config import Config
from extensions import db
from flask_migrate import Migrate
from routes import main
from models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key') # Add this line

    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    register_resources(app)
    register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

def register_resources(app):
    app.register_blueprint(main)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1',5000)

