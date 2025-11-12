from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_DOCS_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)

    from app import auth, crew, admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(crew.bp)
    app.register_blueprint(admin.bp)

    with app.app_context():
        db.create_all()

    return app
