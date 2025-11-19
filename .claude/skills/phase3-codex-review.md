# Phase 3 Codex Review Skill

## Description
Comprehensive code review for the Ship Maintenance Tracking Application (ship-MTA-draft). This skill performs multi-dimensional analysis including security, code quality, performance, architecture, and best practices.

## Usage
Invoke this skill to perform a thorough code review of the codebase and generate actionable improvement recommendations.

## Review Objectives

You are conducting a Phase 3 code review for a Flask-based Ship Maintenance Tracking Application. Your goal is to identify improvements across multiple dimensions and provide actionable recommendations.

### Context
- **Application**: Ship Maintenance Tracking web app
- **Stack**: Python/Flask, SQLAlchemy, Bootstrap, Pillow, python-docx
- **Purpose**: Mobile-first work item submission with photo uploads and document generation
- **Users**: 6 crew members + admin users
- **Deployment**: Railway.app with PostgreSQL

### Review Dimensions

Execute specialized agents for each review dimension:

1. **Security Review** - Identify security vulnerabilities and risks
2. **Code Quality Review** - Assess code organization, readability, and maintainability
3. **Performance Review** - Find performance bottlenecks and optimization opportunities
4. **Architecture Review** - Evaluate design patterns and architectural decisions
5. **Best Practices Review** - Check adherence to Flask/Python best practices

### Instructions

1. **Launch parallel review agents** for each dimension using the Task tool
2. **Aggregate findings** from all agents
3. **Prioritize recommendations** by impact and effort
4. **Generate comprehensive report** with:
   - Executive Summary
   - Critical Issues (fix immediately)
   - High Priority Issues (fix before production)
   - Medium Priority Issues (fix soon)
   - Low Priority Issues (nice to have)
   - Code examples and solutions
   - Implementation roadmap

### Key Files to Review

**Core Application:**
- `app/__init__.py` - Flask app initialization
- `app/models.py` - Database models
- `app/auth.py` - Authentication logic
- `app/crew.py` - Crew submission routes
- `app/admin.py` - Admin management routes
- `app/docx_generator.py` - Document generation
- `app/utils.py` - Utility functions
- `config.py` - Configuration

**Templates:**
- All files in `app/templates/`

**Static Assets:**
- `app/static/css/style.css`
- `app/static/js/main.js`

### Deliverables

1. **Comprehensive Review Report** (Markdown)
2. **Priority Matrix** (Critical/High/Medium/Low)
3. **Quick Wins List** (Easy fixes with high impact)
4. **Security Checklist** (Vulnerabilities found)
5. **Refactoring Recommendations** (Code improvements)
6. **Performance Optimization Guide** (Speed improvements)
7. **Action Plan** (Step-by-step implementation guide)

### Output Format

Generate a detailed report following this structure:

```markdown
# Phase 3 Code Review Report - Ship MTA Draft
**Review Date**: [Current Date]
**Reviewer**: Claude Code (Automated Review)

## Executive Summary
[3-5 paragraphs summarizing key findings]

## Critical Issues 🔴
[Issues that must be fixed immediately]

## High Priority Issues 🟡
[Issues to fix before production]

## Medium Priority Issues 🟠
[Issues to address soon]

## Low Priority Issues 🟢
[Nice to have improvements]

## Quick Wins ⚡
[Easy fixes with high impact]

## Detailed Findings

### 1. Security Review
[Detailed security findings]

### 2. Code Quality Review
[Detailed quality findings]

### 3. Performance Review
[Detailed performance findings]

### 4. Architecture Review
[Detailed architecture findings]

### 5. Best Practices Review
[Detailed best practices findings]

## Recommendations Summary
[Consolidated recommendations]

## Implementation Roadmap
[Step-by-step action plan]
```

### Review Agents to Launch

Use the Task tool to launch these agents in parallel:

1. **Security Agent**: Focus on OWASP Top 10, authentication, authorization, input validation, SQL injection, XSS, CSRF, file upload security, session management, secrets management

2. **Code Quality Agent**: Focus on code organization, DRY principle, function complexity, naming conventions, documentation, error handling, logging, testing coverage

3. **Performance Agent**: Focus on database queries, N+1 queries, image processing, caching opportunities, async operations, memory usage, file I/O optimization

4. **Architecture Agent**: Focus on separation of concerns, design patterns, scalability, modularity, dependency management, configuration management, database design

5. **Best Practices Agent**: Focus on Flask patterns, Python idioms, PEP 8 compliance, type hints, docstrings, package structure, deployment readiness

### Success Criteria

A successful review will:
- Identify all security vulnerabilities
- Provide code examples for fixes
- Prioritize issues by severity and effort
- Offer practical, actionable recommendations
- Include estimated time for each fix
- Reference specific file paths and line numbers
- Suggest tools and libraries where applicable
- Consider the production deployment context (Railway)

Now begin the comprehensive code review by launching the specialized review agents.
