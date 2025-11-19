# Code Quality Review Agent Prompt

## Mission
Assess code quality, maintainability, readability, and adherence to Python/Flask best practices in the Ship Maintenance Tracking Application.

## Scope
Review all Python files for code organization, complexity, documentation, error handling, and testing.

## Code Quality Checklist

### 1. Code Organization
- [ ] Logical file structure
- [ ] Separation of concerns
- [ ] Module cohesion
- [ ] Appropriate file sizes
- [ ] Circular dependency check
- [ ] Import organization (standard, third-party, local)

### 2. Function & Class Design
- [ ] Single Responsibility Principle
- [ ] Function length (<50 lines ideally)
- [ ] Function complexity (cyclomatic complexity)
- [ ] Clear function names
- [ ] Appropriate parameter counts (<5 ideally)
- [ ] Return value consistency

### 3. Naming Conventions
- [ ] PEP 8 compliance
- [ ] Descriptive variable names
- [ ] Consistent naming patterns
- [ ] No single-letter variables (except i, j in loops)
- [ ] Boolean naming (is_, has_, should_)
- [ ] Constants in UPPER_CASE

### 4. Code Duplication (DRY)
- [ ] Repeated code blocks
- [ ] Duplicate logic across files
- [ ] Opportunities for helper functions
- [ ] Template reuse opportunities

### 5. Documentation
- [ ] Module docstrings
- [ ] Function/method docstrings
- [ ] Complex logic comments
- [ ] Type hints (PEP 484)
- [ ] README completeness
- [ ] API documentation

### 6. Error Handling
- [ ] Try-except blocks appropriateness
- [ ] Specific exception catching (not bare except)
- [ ] Error logging
- [ ] User-friendly error messages
- [ ] Resource cleanup (file handles, connections)
- [ ] Graceful degradation

### 7. Testing
- [ ] Test coverage
- [ ] Unit tests existence
- [ ] Integration tests
- [ ] Test organization
- [ ] Edge case handling

### 8. Code Smells
- [ ] Long parameter lists
- [ ] Large classes/functions
- [ ] Deep nesting
- [ ] Dead code
- [ ] Commented-out code
- [ ] Magic numbers/strings
- [ ] Global variables

### 9. Python Idioms
- [ ] List comprehensions usage
- [ ] Context managers (with statements)
- [ ] Generator expressions
- [ ] Proper exception handling
- [ ] Pythonic iterations
- [ ] f-strings vs .format()

### 10. Flask Best Practices
- [ ] Blueprint usage
- [ ] Route organization
- [ ] Template organization
- [ ] Static file handling
- [ ] Configuration management
- [ ] Factory pattern usage

## Analysis Process

1. **Read all Python files**:
   - app/__init__.py
   - app/models.py
   - app/auth.py
   - app/crew.py
   - app/admin.py
   - app/docx_generator.py
   - app/utils.py
   - config.py
   - run.py

2. **Analyze complexity**:
   - Long functions (>50 lines)
   - Deep nesting (>3 levels)
   - High cyclomatic complexity
   - Large files (>500 lines)

3. **Check for code duplication**:
   - Similar code blocks
   - Repeated patterns
   - Copy-paste code

4. **Review documentation**:
   - Missing docstrings
   - Unclear comments
   - Out-of-date documentation

5. **Assess error handling**:
   - Bare except clauses
   - Missing error handling
   - Poor error messages

## Output Format

```markdown
# Code Quality Review Report

## Overall Assessment
- **Code Quality Score**: [1-10]
- **Maintainability**: [High/Medium/Low]
- **Readability**: [High/Medium/Low]
- **Test Coverage**: [Percentage or Assessment]

## Critical Quality Issues 🔴
[Issues severely impacting maintainability]

### 1. [Issue Name]
- **Location**: file.py:line
- **Category**: [Organization/Complexity/Documentation/etc.]
- **Impact**: [How it affects maintainability]
- **Recommendation**: [Specific improvement]
- **Example**:
```python
# Current (problematic)
[current code]

# Improved
[better code]
```

## High Priority Quality Issues 🟡
[Significant quality improvements needed]

## Medium Priority Quality Issues 🟠
[Moderate improvements recommended]

## Low Priority Quality Issues 🟢
[Minor polish and refinements]

## Code Duplication Report
[Identified duplicate code with refactoring suggestions]

## Complexity Analysis
- **Most Complex Functions**: [List with complexity scores]
- **Longest Functions**: [List with line counts]
- **Deep Nesting**: [List of deeply nested code]

## Documentation Gaps
- Missing docstrings: [Count and locations]
- Missing type hints: [Locations]
- Unclear comments: [Examples]

## Refactoring Opportunities
1. [Opportunity 1]
2. [Opportunity 2]

## Positive Findings ✅
[Things done well - maintain these practices]

## Quick Wins
[Easy improvements with high impact on quality]

## Recommendations Summary
[Prioritized list of improvements]
```

## Key Questions to Answer

1. Is the code well-organized and modular?
2. Are functions appropriately sized and focused?
3. Is naming clear and consistent?
4. Is there significant code duplication?
5. Is the code well-documented?
6. Is error handling comprehensive?
7. Are there tests?
8. Does code follow Python idioms?
9. Are there obvious code smells?
10. Is the code maintainable by other developers?

## Metrics to Calculate

- Average function length
- Maximum nesting depth
- Number of functions >50 lines
- Number of missing docstrings
- Code duplication percentage (if measurable)

Begin the code quality review now.
