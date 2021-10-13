from flask_sqlalchemy import SQLAlchemy 
import flask_login

db = SQLAlchemy()
login_manager = flask_login.LoginManager()