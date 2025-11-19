from flask import Flask, send_from_directory, session, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging


db = SQLAlchemy()
migrate = Migrate()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_DOCS_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)

    from app import auth, crew, admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(crew.bp)
    app.register_blueprint(admin.bp)

    # Health check endpoint for monitoring
    @app.route('/health')
    def health_check():
        """Health check endpoint for Railway and monitoring systems.

        Tests database connectivity and returns JSON status.
        Returns 200 if healthy, 500 if unhealthy.
        """
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Test database connectivity
            db.session.execute(db.text('SELECT 1'))
            db.session.commit()

            return {
                'status': 'healthy',
                'database': 'connected',
                'environment': app.config['FLASK_ENV']
            }, 200
        except Exception as e:
            logger.error(f'Health check failed: {str(e)}')
            return {
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }, 500

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

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        """Handle 404 errors with custom template."""
        logger.warning(f'Page not found: {request.url}')
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 errors with custom template and logging."""
        logger.error(f'Internal server error: {str(error)}', exc_info=True)
        db.session.rollback()  # Rollback any failed database transactions
        return render_template('500.html'), 500

    # NOTE: Database migrations are now handled by Flask-Migrate
    # Use `flask db upgrade` instead of db.create_all()
    # Keeping this for backward compatibility in development only
    with app.app_context():
        if app.config['FLASK_ENV'] == 'development':
            db.create_all()

    return app
