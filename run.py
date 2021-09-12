from flask import Flask, Blueprint
import flask_login
from extensions import db, login_manager




def create_app(config_file='settings.py'):
    app = Flask(__name__)


    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():

        from routes import main

        app.register_blueprint(main)



        return app
