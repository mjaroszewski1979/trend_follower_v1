from flask import Flask, Blueprint
import flask_login
from extensions import db, login_manager



# Creating an application object using factory pattern
def create_app(config_file='settings.py'):
    app = Flask(__name__)


    # Loading settings
    app.config.from_pyfile(config_file)

    # Initializing extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Creating neccesary application context
    with app.app_context():

        from routes import main

        # Registering main blueprint
        app.register_blueprint(main)



        return app
