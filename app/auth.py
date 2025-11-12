from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app


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
def crew_login():
    """Crew member login."""
    if request.method == 'POST':
        password = request.form.get('password')
        crew_name = request.form.get('crew_name')

        if password == current_app.config['CREW_PASSWORD'] and crew_name:
            session['crew_authenticated'] = True
            session['crew_name'] = crew_name
            session.permanent = True
            return redirect(url_for('crew.submit_form'))
        else:
            flash('Invalid password or crew name not selected', 'danger')

    crew_members = current_app.config['CREW_MEMBERS']
    return render_template('login.html', crew_members=crew_members)


@bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (username == current_app.config['ADMIN_USERNAME'] and 
            password == current_app.config['ADMIN_PASSWORD']):
            session['is_admin'] = True
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
