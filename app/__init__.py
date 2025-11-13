from flask import Flask, send_from_directory, session, redirect, url_for
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

    # Shared upload endpoint for both admin and crew
    @app.route('/uploads/<filename>')
    def serve_upload(filename):
        """Serve uploaded photos (accessible to both admin and crew)."""
        # Check if user is authenticated (either admin or crew)
        if not session.get('is_admin') and not session.get('crew_authenticated'):
            return redirect(url_for('auth.crew_login'))
        
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app
