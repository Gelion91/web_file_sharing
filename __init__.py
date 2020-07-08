from flask import Flask
from main.views import blueprint as main_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(main_blueprint)


    return app
