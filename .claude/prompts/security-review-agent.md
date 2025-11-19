# Security Review Agent Prompt

## Mission
Perform a comprehensive security audit of the Ship Maintenance Tracking Application, focusing on OWASP Top 10 vulnerabilities and production security readiness.

## Scope
Review all Python backend files, authentication mechanisms, file uploads, database queries, session management, and configuration.

## Security Checklist

### 1. Authentication & Authorization
- [ ] Password storage (hashing, salting)
- [ ] Session management (secure cookies, timeout, regeneration)
- [ ] Password strength requirements
- [ ] Brute force protection
- [ ] Admin vs crew authorization checks
- [ ] Session fixation vulnerabilities
- [ ] Logout functionality completeness

### 2. Input Validation & Sanitization
- [ ] Form input validation (client & server-side)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output escaping)
- [ ] File upload validation (type, size, content)
- [ ] Path traversal prevention
- [ ] Command injection prevention
- [ ] LDAP injection prevention

### 3. File Upload Security
- [ ] File type validation (whitelist)
- [ ] File size limits
- [ ] Filename sanitization
- [ ] Content-type verification
- [ ] Malware scanning consideration
- [ ] Storage location security (outside webroot)
- [ ] Image processing vulnerabilities (PIL/Pillow)

### 4. CSRF Protection
- [ ] CSRF tokens on forms
- [ ] SameSite cookie attributes
- [ ] Referer validation

### 5. Secrets Management
- [ ] Environment variables usage
- [ ] Hardcoded credentials check
- [ ] SECRET_KEY strength and randomness
- [ ] API keys and tokens protection
- [ ] .env file in .gitignore

### 6. Database Security
- [ ] SQL injection prevention
- [ ] Database connection security
- [ ] Sensitive data encryption
- [ ] Database user permissions
- [ ] ORM usage (SQLAlchemy best practices)

### 7. Error Handling & Logging
- [ ] Information disclosure in errors
- [ ] Stack trace exposure
- [ ] Debug mode in production
- [ ] Logging sensitive data
- [ ] Error message security

### 8. HTTP Security Headers
- [ ] X-Frame-Options
- [ ] X-Content-Type-Options
- [ ] Content-Security-Policy
- [ ] Strict-Transport-Security
- [ ] X-XSS-Protection

### 9. Dependency Security
- [ ] requirements.txt versions pinned
- [ ] Known vulnerabilities in dependencies
- [ ] Outdated packages
- [ ] Unnecessary dependencies

### 10. Configuration Security
- [ ] Debug mode disabled in production
- [ ] HTTPS enforcement
- [ ] Secure session configuration
- [ ] Database URL security
- [ ] Environment-specific configs

## Analysis Process

1. **Read all core files**:
   - config.py
   - app/__init__.py
   - app/auth.py
   - app/crew.py
   - app/admin.py
   - app/models.py
   - app/utils.py
   - requirements.txt

2. **Search for security anti-patterns**:
   - `password` (check hashing)
   - `SECRET_KEY` (check randomness)
   - `session` (check security)
   - `execute` or raw SQL (check injection)
   - `eval` or `exec` (dangerous)
   - `.format` or `%` with user input
   - File operations with user input

3. **Check authentication flows**:
   - Login process
   - Logout process
   - Session creation
   - Authorization decorators

4. **Review file upload logic**:
   - File validation
   - Storage mechanism
   - Retrieval mechanism
   - Permission checks

## Output Format

```markdown
# Security Review Report

## Critical Vulnerabilities 🔴
[Issues requiring immediate attention]

### 1. [Vulnerability Name]
- **Location**: file.py:line
- **Severity**: Critical
- **Risk**: [Description of risk]
- **Exploit Scenario**: [How it could be exploited]
- **Fix**: [Specific code changes needed]
- **Example**:
```python
# Before (vulnerable)
[current code]

# After (secure)
[fixed code]
```

## High Risk Issues 🟡
[Security issues to fix before production]

## Medium Risk Issues 🟠
[Security improvements recommended]

## Low Risk Issues 🟢
[Minor security enhancements]

## Security Best Practices Recommendations
[General recommendations]

## Security Checklist for Production
- [ ] Item 1
- [ ] Item 2

## References
- OWASP Top 10 2021
- Flask Security Best Practices
- Python Security Guidelines
```

## Key Questions to Answer

1. Is user authentication secure?
2. Are sessions managed securely?
3. Can SQL injection occur anywhere?
4. Is XSS possible in any template?
5. Are file uploads validated properly?
6. Are secrets managed securely?
7. Is CSRF protection implemented?
8. Are error messages leaking information?
9. Are security headers configured?
10. Are dependencies up-to-date and secure?

Begin the security review now.
