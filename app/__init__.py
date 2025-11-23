from flask import Flask, send_from_directory, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


db = SQLAlchemy()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Security headers middleware
    @app.after_request
    def set_security_headers(response):
        """Add security headers to all responses."""
        security_headers = app.config.get('SECURITY_HEADERS', {})
        for header, value in security_headers.items():
            response.headers[header] = value
        return response

    # Input sanitization helper
    @app.template_filter('sanitize')
    def sanitize_html(text):
        """Sanitize HTML content to prevent XSS."""
        import bleach
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li']
        allowed_attrs = {}
        return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)

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
