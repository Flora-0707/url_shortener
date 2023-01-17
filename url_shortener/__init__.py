from flask import Flask
from .extensions import db
from .routes import shortener

def create_app(config_file = 'settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    from . import models
    with app.app_context():
        db.create_all()

    app.register_blueprint(shortener)

    return app