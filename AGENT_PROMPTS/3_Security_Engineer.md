# Agent 3: Security Engineer

## Branch Information
**Branch Name:** `claude/security-hardening`
**Estimated Time:** 3-5 hours
**Priority:** CRITICAL

## Role & Responsibilities
You are the Security Engineer responsible for auditing and hardening the application's security posture. Your goal is to identify and fix security vulnerabilities before production deployment.

## Mission Objective
Perform a comprehensive security audit and implement critical security hardening measures including CSRF protection, input validation, secure headers, rate limiting, and secrets management.

## Current Security Issues

Based on initial analysis, the following security concerns exist:

1. **Missing CSRF Protection** - Forms not protected against Cross-Site Request Forgery
2. **Weak Input Validation** - Insufficient validation on user inputs
3. **Default Credentials** - Hardcoded default passwords in config.py
4. **Missing Security Headers** - No security headers (CSP, X-Frame-Options, etc.)
5. **No Rate Limiting** - Login endpoints vulnerable to brute force
6. **SQL Injection Risk** - Some queries use string formatting instead of parameterized queries
7. **Path Traversal Risk** - File upload/serving may be vulnerable
8. **Missing Audit Logging** - No logging of security events

## Step-by-Step Tasks

### Phase 1: Security Audit (1 hour)

1. **Review all routes for vulnerabilities:**
   ```bash
   # Create security audit checklist
   grep -r "request.args.get" app/
   grep -r "request.form.get" app/
   grep -r ".format(" app/
   grep -r "f\"" app/
   grep -r "%" app/
   ```

2. **Identify injection points:**
   - Review `app/admin.py` - database queries
   - Review `app/crew.py` - form inputs
   - Review `app/utils.py` - file operations
   - Review SQL queries for parameterization

3. **Check authentication/authorization:**
   - Review `@admin_required` decorator
   - Review `@crew_required` decorator
   - Check for authorization bypasses
   - Verify session security

4. **Create `SECURITY_AUDIT.md` documenting all findings**

### Phase 2: CSRF Protection (1 hour)

1. **Install Flask-WTF for CSRF protection:**
   ```bash
   pip install Flask-WTF
   ```

2. **Update `requirements.txt`:**
   ```
   Flask-WTF==1.2.1
   ```

3. **Configure CSRF in `app/__init__.py`:**
   ```python
   from flask_wtf.csrf import CSRFProtect

   csrf = CSRFProtect()

   def create_app():
       app = Flask(__name__)
       # ... existing config ...
       csrf.init_app(app)
       return app
   ```

4. **Add CSRF tokens to all forms:**

   Update these templates:
   - `app/templates/login.html`
   - `app/templates/admin_login.html`
   - `app/templates/crew_form.html`
   - `app/templates/admin_view_item.html` (edit form)
   - `app/templates/crew_edit.html`

   Add to each form:
   ```html
   <form method="POST">
       {{ csrf_token() }}
       <!-- rest of form -->
   </form>
   ```

   Or using hidden input:
   ```html
   <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
   ```

5. **Update AJAX requests to include CSRF token:**

   In `app/static/js/photo-upload.js` and any AJAX calls:
   ```javascript
   // Add CSRF token to fetch/AJAX requests
   fetch(url, {
       method: 'POST',
       headers: {
           'X-CSRFToken': getCsrfToken()
       },
       body: formData
   });

   function getCsrfToken() {
       return document.querySelector('meta[name="csrf-token"]').content;
   }
   ```

6. **Add CSRF meta tag to `app/templates/base.html`:**
   ```html
   <head>
       <meta name="csrf-token" content="{{ csrf_token() }}">
   </head>
   ```

### Phase 3: Input Validation & Sanitization (1-2 hours)

1. **Create `app/validators.py`:**

   ```python
   """Input validation functions."""
   import re
   from werkzeug.exceptions import BadRequest

   def validate_item_number(item_number: str) -> str:
       """Validate and sanitize item number."""
       if not item_number:
           raise BadRequest("Item number is required")

       # Allow only alphanumeric, underscore, dash
       if not re.match(r'^[A-Z0-9_-]+$', item_number):
           raise BadRequest("Invalid item number format")

       if len(item_number) > 50:
           raise BadRequest("Item number too long")

       return item_number

   def validate_text_field(text: str, field_name: str, min_len: int = 1, max_len: int = 500) -> str:
       """Validate and sanitize text input."""
       if not text or not text.strip():
           raise BadRequest(f"{field_name} is required")

       text = text.strip()

       if len(text) < min_len:
           raise BadRequest(f"{field_name} must be at least {min_len} characters")

       if len(text) > max_len:
           raise BadRequest(f"{field_name} must be less than {max_len} characters")

       return text

   def validate_filename(filename: str) -> str:
       """Validate and sanitize filename to prevent path traversal."""
       if not filename:
           raise BadRequest("Filename is required")

       # Remove path separators
       filename = filename.replace('/', '').replace('\\', '').replace('..', '')

       # Allow only safe characters
       if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
           raise BadRequest("Invalid filename")

       return filename

   def validate_status(status: str, allowed_statuses: list) -> str:
       """Validate status is in allowed list."""
       if status not in allowed_statuses:
           raise BadRequest(f"Invalid status: {status}")
       return status
   ```

2. **Update `app/crew.py` with validation:**

   ```python
   from app.validators import validate_item_number, validate_text_field

   @bp.route('/submit', methods=['POST'])
   @crew_required
   def submit_form():
       try:
           # Validate inputs
           item_number = validate_item_number(request.form.get('item_number', ''))
           location = validate_text_field(request.form.get('location'), 'Location', max_len=200)
           description = validate_text_field(request.form.get('description'), 'Description', max_len=500)
           detail = validate_text_field(request.form.get('detail'), 'Detail', max_len=2000)
           # ... rest of logic
       except BadRequest as e:
           flash(str(e), 'danger')
           return redirect(url_for('crew.submit_form'))
   ```

3. **Update `app/admin.py` with validation:**

   Add validation to:
   - `edit_item()` route - validate all form inputs
   - `assign_item()` route - validate crew member
   - `update_status()` route - validate status
   - `serve_upload()` route - validate filename

4. **Sanitize user-generated content in templates:**

   Jinja2 auto-escapes by default, but verify:
   ```html
   <!-- Good (auto-escaped): -->
   <p>{{ work_item.description }}</p>

   <!-- Bad (unsafe, don't use): -->
   <p>{{ work_item.description | safe }}</p>
   ```

### Phase 4: Secure Headers & Configuration (30 minutes)

1. **Install Flask-Talisman for security headers:**
   ```bash
   pip install flask-talisman
   ```

2. **Configure security headers in `app/__init__.py`:**
   ```python
   from flask_talisman import Talisman

   def create_app():
       app = Flask(__name__)
       # ... existing config ...

       # Security headers
       if app.config['FLASK_ENV'] == 'production':
           Talisman(app,
               force_https=True,
               strict_transport_security=True,
               content_security_policy={
                   'default-src': "'self'",
                   'script-src': ["'self'", "'unsafe-inline'"],
                   'style-src': ["'self'", "'unsafe-inline'"],
                   'img-src': ["'self'", 'data:', 'https:'],
               },
               session_cookie_secure=True,
               session_cookie_httponly=True,
               session_cookie_samesite='Lax',
           )

       return app
   ```

3. **Update `config.py` with secure session settings:**
   ```python
   # Session Security
   SESSION_COOKIE_SECURE = FLASK_ENV == 'production'  # HTTPS only in production
   SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
   SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
   PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # Already exists
   ```

### Phase 5: Rate Limiting (1 hour)

1. **Install Flask-Limiter:**
   ```bash
   pip install Flask-Limiter
   ```

2. **Configure rate limiting in `app/__init__.py`:**
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   limiter = Limiter(
       app=app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"],
       storage_uri="memory://"  # Or use Redis for production
   )
   ```

3. **Add rate limiting to sensitive routes:**

   Update `app/auth.py`:
   ```python
   from app import limiter

   @bp.route('/crew/login', methods=['POST'])
   @limiter.limit("5 per minute")  # Prevent brute force
   def crew_login():
       # ... existing code ...

   @bp.route('/admin/login', methods=['POST'])
   @limiter.limit("3 per minute")  # Stricter for admin
   def admin_login():
       # ... existing code ...
   ```

4. **Add rate limiting to photo upload:**
   ```python
   @bp.route('/crew/submit', methods=['POST'])
   @limiter.limit("10 per hour")  # Prevent spam uploads
   @crew_required
   def submit_form():
       # ... existing code ...
   ```

### Phase 6: Secure File Handling (1 hour)

1. **Update `app/utils.py` - secure filename handling:**
   ```python
   from werkzeug.utils import secure_filename
   import os

   def validate_and_secure_filename(filename: str) -> str:
       """Validate and secure filename to prevent path traversal."""
       # Use werkzeug's secure_filename
       filename = secure_filename(filename)

       # Additional validation
       if not filename:
           raise ValueError("Invalid filename")

       # Prevent directory traversal
       if '..' in filename or '/' in filename or '\\' in filename:
           raise ValueError("Invalid filename - path traversal detected")

       # Limit filename length
       if len(filename) > 255:
           raise ValueError("Filename too long")

       return filename
   ```

2. **Update photo upload in `app/crew.py`:**
   ```python
   from app.utils import validate_and_secure_filename

   # In submit_form():
   for photo_file in photo_files:
       if photo_file and allowed_file(photo_file.filename):
           # Secure the filename
           safe_filename = validate_and_secure_filename(photo_file.filename)
           filename = generate_unique_filename(safe_filename)
           # ... rest of upload logic
   ```

3. **Update file serving in `app/admin.py`:**
   ```python
   @bp.route('/uploads/<filename>')
   @admin_required
   def serve_upload(filename):
       """Serve uploaded photos securely."""
       # Validate filename to prevent path traversal
       safe_filename = secure_filename(filename)

       # Ensure file exists and is in upload folder
       file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)

       # Prevent path traversal
       if not os.path.abspath(file_path).startswith(os.path.abspath(current_app.config['UPLOAD_FOLDER'])):
           abort(403)

       return send_from_directory(current_app.config['UPLOAD_FOLDER'], safe_filename)
   ```

### Phase 7: Secrets Management (30 minutes)

1. **Update `config.py` to require secrets in production:**
   ```python
   class Config:
       FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

       # Security - require secrets in production
       if FLASK_ENV == 'production':
           required_vars = ['SECRET_KEY', 'ADMIN_PASSWORD', 'CREW_PASSWORD']
           missing = [var for var in required_vars if not os.environ.get(var)]
           if missing:
               raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

       SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

       # Warn about default credentials
       CREW_PASSWORD = os.environ.get('CREW_PASSWORD') or 'crew350'
       ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin350'

       if FLASK_ENV == 'production':
           if CREW_PASSWORD == 'crew350' or ADMIN_PASSWORD == 'admin350':
               raise RuntimeError("CRITICAL: Default passwords detected in production!")
   ```

2. **Update `.env.example` with security notes:**
   ```bash
   # SECURITY: CHANGE ALL DEFAULT VALUES IN PRODUCTION!

   # Flask Configuration
   FLASK_ENV=production
   SECRET_KEY=  # REQUIRED: Generate with: python -c 'import secrets; print(secrets.token_hex(32))'

   # Authentication - CHANGE THESE!
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=  # REQUIRED: Use strong password (16+ characters)
   CREW_PASSWORD=  # REQUIRED: Use strong password (16+ characters)

   # Database
   DATABASE_URL=  # Provided by Railway PostgreSQL

   # Cloudinary (if using cloud storage)
   CLOUDINARY_CLOUD_NAME=
   CLOUDINARY_API_KEY=
   CLOUDINARY_API_SECRET=
   ```

3. **Add security documentation to `README.md`:**

   Add a "Security" section explaining:
   - How to generate secure SECRET_KEY
   - Password requirements
   - HTTPS requirement for production
   - Regular security updates

### Phase 8: Security Logging (30 minutes)

1. **Create `app/security_logger.py`:**
   ```python
   """Security event logging."""
   import logging
   from flask import request
   from datetime import datetime

   logger = logging.getLogger('security')

   def log_security_event(event_type: str, user: str, details: str):
       """Log security-related events."""
       logger.warning(
           f"SECURITY: {event_type} | User: {user} | "
           f"IP: {request.remote_addr} | Details: {details} | "
           f"Time: {datetime.utcnow()}"
       )

   def log_failed_login(username: str, user_type: str):
       """Log failed login attempt."""
       log_security_event('FAILED_LOGIN', username, f'Failed {user_type} login')

   def log_successful_login(username: str, user_type: str):
       """Log successful login."""
       log_security_event('LOGIN', username, f'Successful {user_type} login')

   def log_unauthorized_access(user: str, resource: str):
       """Log unauthorized access attempt."""
       log_security_event('UNAUTHORIZED', user, f'Attempted access to {resource}')
   ```

2. **Add logging to `app/auth.py`:**
   ```python
   from app.security_logger import log_failed_login, log_successful_login

   @bp.route('/admin/login', methods=['POST'])
   def admin_login():
       # ... existing code ...
       if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
           log_successful_login(username, 'admin')
           # ... login logic
       else:
           log_failed_login(username, 'admin')
           flash('Invalid credentials', 'danger')
   ```

3. **Configure logging in `app/__init__.py`:**
   ```python
   import logging

   # Security logging configuration
   security_logger = logging.getLogger('security')
   security_logger.setLevel(logging.WARNING)
   handler = logging.FileHandler('security.log')
   handler.setFormatter(logging.Formatter(
       '%(asctime)s - %(levelname)s - %(message)s'
   ))
   security_logger.addHandler(handler)
   ```

## Files You MUST Modify/Create

### Create:
- `app/validators.py` - Input validation functions
- `app/security_logger.py` - Security event logging
- `SECURITY_AUDIT.md` - Document security findings
- `.env.example` - Updated with security notes

### Modify:
- `app/__init__.py` - Add CSRF, Talisman, rate limiting
- `app/auth.py` - Add rate limiting and security logging
- `app/crew.py` - Add input validation
- `app/admin.py` - Add input validation and secure file serving
- `app/utils.py` - Secure filename handling
- `config.py` - Secure session config, require secrets
- `requirements.txt` - Add Flask-WTF, Flask-Talisman, Flask-Limiter
- All templates - Add CSRF tokens
- `README.md` - Add security documentation

### DO NOT Modify:
- Database models (unless adding security fields)
- Static assets (unless updating AJAX for CSRF)

## Quality Checklist

### CSRF Protection:
- [ ] Flask-WTF installed and configured
- [ ] CSRF tokens in all forms
- [ ] CSRF tokens in AJAX requests
- [ ] CSRF meta tag in base template

### Input Validation:
- [ ] Validators module created
- [ ] All user inputs validated
- [ ] SQL injection prevented (parameterized queries)
- [ ] Path traversal prevented
- [ ] XSS prevented (template escaping)

### Security Headers:
- [ ] Flask-Talisman configured
- [ ] HTTPS enforced in production
- [ ] Secure session cookies
- [ ] CSP headers configured

### Rate Limiting:
- [ ] Flask-Limiter installed
- [ ] Login endpoints rate limited
- [ ] Upload endpoints rate limited
- [ ] Rate limits appropriate (not too strict)

### Secrets Management:
- [ ] Secrets required in production
- [ ] Default passwords blocked in production
- [ ] .env.example updated
- [ ] README security docs added

### Logging:
- [ ] Security logger created
- [ ] Failed logins logged
- [ ] Successful logins logged
- [ ] Unauthorized access logged

### Testing:
- [ ] CSRF protection tested (forms reject without token)
- [ ] Input validation tested (rejects invalid input)
- [ ] Rate limiting tested (blocks after limit)
- [ ] File upload security tested (rejects ../.. paths)
- [ ] Security headers verified (check with securityheaders.com)

## Security Testing Commands

```bash
# Test CSRF protection
curl -X POST http://localhost:5001/crew/submit -d "..."
# Should fail without CSRF token

# Test rate limiting
for i in {1..10}; do curl http://localhost:5001/auth/admin/login; done
# Should block after limit

# Test input validation
curl -X POST http://localhost:5001/crew/submit -d "location=<script>alert('xss')</script>"
# Should reject

# Check security headers
curl -I https://your-app.railway.app
# Should see X-Frame-Options, CSP, HSTS headers
```

## Success Criteria

- ✅ CSRF protection on all forms
- ✅ All user inputs validated and sanitized
- ✅ Security headers configured
- ✅ Rate limiting on sensitive endpoints
- ✅ Secure file handling (no path traversal)
- ✅ Secrets required in production
- ✅ Security events logged
- ✅ No SQL injection vulnerabilities
- ✅ Security audit documented

## Deliverables

1. CSRF protection implemented
2. Input validation module
3. Security headers configured
4. Rate limiting on endpoints
5. Secure file handling
6. Security logging
7. `SECURITY_AUDIT.md` report
8. Updated documentation

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/3.0.x/security/)
- [Flask-WTF CSRF](https://flask-wtf.readthedocs.io/en/1.2.x/csrf/)
- [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
- [Security Headers](https://securityheaders.com/)

## Notes

- Test all changes locally before deploying
- Don't break existing functionality
- Security must not compromise usability
- Document all changes in SECURITY_AUDIT.md
- Run security scanner (Bandit) if time permits

---

**Ready to start?** Begin with Phase 1 (Security Audit) to understand the current state, then work through each phase systematically!
