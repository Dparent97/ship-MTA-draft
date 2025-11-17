from flask import Flask, send_from_directory, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os


db = SQLAlchemy()
cache = Cache()


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure caching
    app.config['CACHE_TYPE'] = 'SimpleCache'  # In-memory cache (use Redis in production)
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes default timeout

    db.init_app(app)
    cache.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_DOCS_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)

    from app import auth, crew, admin
    from app.performance import init_performance_monitoring

    app.register_blueprint(auth.bp)
    app.register_blueprint(crew.bp)
    app.register_blueprint(admin.bp)

    # Initialize performance monitoring
    init_performance_monitoring(app)

    # Shared upload endpoint for both admin and crew
    @app.route('/uploads/<filename>')
    def serve_upload(filename):
        """Serve uploaded photos (accessible to both admin and crew).
        
        Note: Photos are protected by UUID filenames (not guessable).
        The real security is at the work item level - users must be 
        authenticated to view work items, but once they can see a work
        item, the photos should load without authentication issues.
        """
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app
