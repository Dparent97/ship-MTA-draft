# Architecture Review Agent Prompt

## Mission
Evaluate the architectural design, patterns, scalability, modularity, and long-term maintainability of the Ship Maintenance Tracking Application.

## Scope
Review overall system design, module organization, design patterns, dependency management, database schema, and deployment architecture.

## Architecture Checklist

### 1. Application Structure
- [ ] Blueprint organization
- [ ] Separation of concerns (MVC/MVT pattern)
- [ ] Module cohesion
- [ ] Module coupling
- [ ] Package organization
- [ ] Circular dependency check

### 2. Design Patterns
- [ ] Application factory pattern
- [ ] Repository pattern for data access
- [ ] Service layer pattern
- [ ] Decorator pattern for auth
- [ ] Strategy pattern opportunities
- [ ] Singleton pattern usage (appropriate)

### 3. Database Design
- [ ] Schema normalization
- [ ] Table relationships (1:1, 1:N, N:M)
- [ ] Foreign key constraints
- [ ] Index design
- [ ] Data integrity constraints
- [ ] Migration strategy
- [ ] Schema evolution planning

### 4. Configuration Management
- [ ] Environment-specific configs
- [ ] Secret management strategy
- [ ] Feature flags (if any)
- [ ] Configuration validation
- [ ] Default value appropriateness

### 5. Dependency Management
- [ ] Tight vs loose coupling
- [ ] Dependency injection
- [ ] Third-party library choices
- [ ] Dependency version pinning
- [ ] Circular dependencies
- [ ] Interface segregation

### 6. Modularity & Extensibility
- [ ] New feature addition ease
- [ ] Module independence
- [ ] Interface design
- [ ] Plugin architecture (if needed)
- [ ] Extensibility points
- [ ] Open/Closed principle adherence

### 7. Scalability Design
- [ ] Horizontal scaling readiness
- [ ] Stateless vs stateful components
- [ ] Database connection pooling
- [ ] Caching layer design
- [ ] Load balancing readiness
- [ ] Microservices potential

### 8. Security Architecture
- [ ] Authentication layer design
- [ ] Authorization model
- [ ] Session management architecture
- [ ] Secrets management
- [ ] Security boundaries
- [ ] Defense in depth

### 9. File Storage Architecture
- [ ] Local vs cloud storage
- [ ] Storage abstraction layer
- [ ] Backup strategy
- [ ] Retention policy
- [ ] Storage scalability

### 10. Deployment Architecture
- [ ] Production readiness
- [ ] Environment parity (dev/staging/prod)
- [ ] Configuration management
- [ ] Database migration strategy
- [ ] Zero-downtime deployment
- [ ] Rollback strategy

## Analysis Process

1. **Analyze overall structure**:
   - Review directory layout
   - Assess module organization
   - Check import relationships
   - Identify architectural patterns

2. **Review database schema**:
   - Read app/models.py
   - Analyze table relationships
   - Check normalization
   - Assess scalability

3. **Evaluate design patterns**:
   - Factory pattern in app/__init__.py
   - Blueprint pattern usage
   - Decorator pattern for auth
   - Service layer existence

4. **Assess modularity**:
   - Module responsibilities
   - Inter-module dependencies
   - Code reusability
   - Extension points

5. **Review configuration**:
   - config.py structure
   - Environment variable usage
   - Secret management
   - Production readiness

## Output Format

```markdown
# Architecture Review Report

## Overall Assessment
- **Architecture Grade**: [A-F]
- **Modularity**: [High/Medium/Low]
- **Scalability**: [High/Medium/Low]
- **Maintainability**: [High/Medium/Low]
- **Pattern Usage**: [Appropriate/Mixed/Poor]

## Critical Architecture Issues 🔴
[Fundamental design problems]

### 1. [Issue Name]
- **Component**: [Module or layer]
- **Problem**: [Architectural issue description]
- **Impact**: [How it affects the system]
- **Recommendation**: [Architectural change needed]
- **Diagram** (if helpful):
```
[ASCII diagram showing current vs proposed]
```
- **Migration Path**: [How to transition]

## High Priority Architecture Issues 🟡
[Significant design improvements]

## Medium Priority Architecture Issues 🟠
[Moderate architectural enhancements]

## Low Priority Architecture Issues 🟢
[Minor design refinements]

## Database Schema Analysis

### Current Schema
[Description of current schema]

### Schema Issues
- **Normalization**: [Assessment]
- **Relationships**: [Issues found]
- **Indexes**: [Missing or redundant]
- **Constraints**: [Missing constraints]

### Recommendations
```sql
-- Recommended schema changes
[SQL DDL statements]
```

## Design Pattern Analysis

### Current Patterns
1. [Pattern 1] - [Usage assessment]
2. [Pattern 2] - [Usage assessment]

### Missing Patterns
1. [Pattern] - [Where it would help]

### Pattern Misuse
1. [Issue] - [Better approach]

## Module Dependency Graph
```
[ASCII or description of dependencies]
app/__init__.py
  ├── app/models.py
  ├── app/auth.py
  ├── app/crew.py
  ├── app/admin.py
  └── config.py
```

### Circular Dependencies
[List any circular dependencies]

### Tight Coupling Issues
[List tightly coupled modules]

## Scalability Assessment

### Current Limitations
1. [Limitation 1]
2. [Limitation 2]

### Horizontal Scaling Readiness
- **Stateless Design**: [Yes/No/Partial]
- **Session Storage**: [In-memory/Database/Redis]
- **File Storage**: [Local/Cloud/Hybrid]
- **Database**: [Scalability assessment]

### Bottlenecks at Scale
1. [Bottleneck 1] - [Solution]
2. [Bottleneck 2] - [Solution]

## Configuration Architecture

### Current Approach
[Description]

### Issues
1. [Issue 1]
2. [Issue 2]

### Recommendations
[Better configuration management approach]

## Security Architecture

### Authentication Flow
```
[Diagram or description]
```

### Authorization Model
[Description and assessment]

### Security Boundaries
[Description of security layers]

### Recommendations
[Security architecture improvements]

## Deployment Architecture

### Current Setup
- **Platform**: Railway
- **Database**: PostgreSQL
- **File Storage**: [Current approach]
- **Sessions**: [Storage method]

### Production Readiness
- [ ] Environment configuration
- [ ] Database migrations
- [ ] Secret management
- [ ] Logging
- [ ] Monitoring
- [ ] Backup strategy

### Recommendations
[Deployment architecture improvements]

## Refactoring Recommendations

### Quick Architectural Wins
1. [Win 1] - [Benefit]
2. [Win 2] - [Benefit]

### Long-term Refactoring
1. [Refactoring 1] - [Timeline]
2. [Refactoring 2] - [Timeline]

## Future-Proofing Recommendations

### Extensibility
[How to make the system more extensible]

### Technology Evolution
[Considerations for future tech changes]

### Growth Planning
[Architectural changes needed for growth]

## Positive Architecture Decisions ✅
[Things done well architecturally]

## Architectural Principles Adherence

- **SOLID Principles**: [Assessment]
- **DRY (Don't Repeat Yourself)**: [Assessment]
- **KISS (Keep It Simple)**: [Assessment]
- **YAGNI (You Aren't Gonna Need It)**: [Assessment]
- **Separation of Concerns**: [Assessment]

## Summary Recommendations
[Prioritized list of architectural improvements]
```

## Key Questions to Answer

1. Is the application well-structured?
2. Are appropriate design patterns used?
3. Is the database schema well-designed?
4. Is the system modular and maintainable?
5. Can the system scale horizontally?
6. Is configuration management sound?
7. Are security boundaries well-defined?
8. Is the deployment architecture appropriate?
9. Are there circular dependencies?
10. Is the system extensible for future features?

## Architectural Concerns to Investigate

- Factory pattern implementation
- Blueprint organization
- Service layer existence
- Repository pattern usage
- Database connection management
- Session storage approach
- File storage abstraction
- Configuration management
- Logging architecture
- Error handling strategy

Begin the architecture review now.
