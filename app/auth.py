from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app import limiter


bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    """Landing page - redirect to crew login."""
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))
    elif session.get('crew_authenticated'):
        return redirect(url_for('crew.submit_form'))
    return redirect(url_for('auth.crew_login'))


@bp.route('/crew-login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def crew_login():
    """Crew member login with rate limiting."""
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        crew_name = request.form.get('crew_name', '').strip()

        # Input validation
        if not password or not crew_name:
            flash('Password and crew name are required', 'danger')
            crew_members = current_app.config['CREW_MEMBERS']
            return render_template('login.html', crew_members=crew_members)

        # Validate crew name is in allowed list
        if crew_name not in current_app.config['CREW_MEMBERS']:
            flash('Invalid crew member selection', 'danger')
            crew_members = current_app.config['CREW_MEMBERS']
            return render_template('login.html', crew_members=crew_members)

        if password == current_app.config['CREW_PASSWORD']:
            session['crew_authenticated'] = True
            session['crew_name'] = crew_name
            session.permanent = True
            return redirect(url_for('crew.submit_form'))
        else:
            flash('Invalid password', 'danger')

    crew_members = current_app.config['CREW_MEMBERS']
    return render_template('login.html', crew_members=crew_members)


@bp.route('/admin-login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def admin_login():
    """Admin login with rate limiting."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Input validation
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('admin_login.html')

        # Length validation to prevent excessive input
        if len(username) > 100 or len(password) > 100:
            flash('Invalid credentials', 'danger')
            return render_template('admin_login.html')

        if (username == current_app.config['ADMIN_USERNAME'] and
            password == current_app.config['ADMIN_PASSWORD']):
            session['is_admin'] = True
            session['crew_name'] = 'admin'  # Set for tracking purposes
            session.permanent = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')

    return render_template('admin_login.html')


@bp.route('/logout')
def logout():
    """Logout (crew or admin)."""
    is_admin = session.get('is_admin', False)
    session.clear()

    if is_admin:
        return redirect(url_for('auth.admin_login'))
    return redirect(url_for('auth.crew_login'))
