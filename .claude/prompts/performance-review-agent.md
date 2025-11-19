# Performance Review Agent Prompt

## Mission
Identify performance bottlenecks, optimization opportunities, and scalability concerns in the Ship Maintenance Tracking Application.

## Scope
Review database queries, image processing, file I/O, memory usage, caching opportunities, and async operations.

## Performance Checklist

### 1. Database Performance
- [ ] N+1 query problems
- [ ] Missing database indexes
- [ ] Inefficient queries
- [ ] Eager vs lazy loading
- [ ] Query result caching
- [ ] Connection pooling
- [ ] Transaction management
- [ ] Database query count per request

### 2. Image Processing
- [ ] Resize algorithm efficiency
- [ ] Memory usage during processing
- [ ] Concurrent upload handling
- [ ] Thumbnail generation strategy
- [ ] Image format optimization (JPEG vs WebP)
- [ ] EXIF data handling
- [ ] Processing timeout handling
- [ ] Async processing opportunities

### 3. File I/O Operations
- [ ] File read/write efficiency
- [ ] Large file handling
- [ ] Streaming vs loading into memory
- [ ] Temporary file cleanup
- [ ] Disk space monitoring
- [ ] File access patterns

### 4. Memory Management
- [ ] Memory leaks
- [ ] Large object allocation
- [ ] Generator usage for large datasets
- [ ] Session data size
- [ ] Upload buffer size
- [ ] Document generation memory usage

### 5. Caching Opportunities
- [ ] Database query caching
- [ ] Template fragment caching
- [ ] Static asset caching
- [ ] Response caching
- [ ] Memoization opportunities
- [ ] CDN usage for static files

### 6. Response Time Optimization
- [ ] Route handler efficiency
- [ ] Template rendering speed
- [ ] Static file delivery
- [ ] Database query optimization
- [ ] Pagination implementation
- [ ] Lazy loading opportunities

### 7. Scalability Concerns
- [ ] Concurrent user handling
- [ ] Database connection limits
- [ ] File storage scalability
- [ ] Session storage scalability
- [ ] Background job processing
- [ ] Load testing readiness

### 8. Asset Optimization
- [ ] CSS minification
- [ ] JavaScript minification
- [ ] Image compression
- [ ] HTTP/2 readiness
- [ ] Asset bundling
- [ ] Lazy loading images

### 9. Algorithm Efficiency
- [ ] Loop optimization
- [ ] Data structure choices
- [ ] Sorting/searching efficiency
- [ ] Regular expression performance
- [ ] String concatenation vs join

### 10. Resource Usage
- [ ] CPU intensive operations
- [ ] Blocking I/O operations
- [ ] Thread pool usage
- [ ] Process pool usage
- [ ] Resource cleanup

## Analysis Process

1. **Read performance-critical files**:
   - app/admin.py (dashboard queries)
   - app/crew.py (file upload handling)
   - app/utils.py (image processing)
   - app/docx_generator.py (document generation)
   - app/models.py (database queries)

2. **Identify database query patterns**:
   - Count queries in each route
   - Look for N+1 problems
   - Check for missing indexes
   - Analyze JOIN operations

3. **Review image processing**:
   - Resize algorithm (LANCZOS, BICUBIC, etc.)
   - Memory allocation for large images
   - Concurrent upload handling
   - Processing queue implementation

4. **Check file operations**:
   - Large file handling
   - Streaming vs memory loading
   - Temporary file cleanup

5. **Analyze caching opportunities**:
   - Repeated database queries
   - Static content
   - Expensive computations

## Output Format

```markdown
# Performance Review Report

## Overall Assessment
- **Performance Grade**: [A-F]
- **Estimated Load Capacity**: [Concurrent users]
- **Major Bottlenecks**: [Count]
- **Quick Win Optimizations**: [Count]

## Critical Performance Issues 🔴
[Issues causing significant slowdowns]

### 1. [Issue Name]
- **Location**: file.py:line or route
- **Impact**: [Estimated performance impact]
- **Current Performance**: [Metric]
- **Expected After Fix**: [Metric]
- **Fix**:
```python
# Current (slow)
[current code]

# Optimized (fast)
[optimized code]
```
- **Estimated Improvement**: [Percentage or time saved]

## High Priority Performance Issues 🟡
[Significant optimization opportunities]

## Medium Priority Performance Issues 🟠
[Moderate performance improvements]

## Low Priority Performance Issues 🟢
[Minor optimizations]

## Database Performance Analysis
- **Total Query Count**: [Per critical route]
- **N+1 Queries**: [List locations]
- **Missing Indexes**: [Recommended indexes]
- **Slow Queries**: [Queries >100ms]

## Image Processing Analysis
- **Average Processing Time**: [Per image]
- **Memory Usage**: [Peak memory per upload]
- **Concurrent Processing**: [Current vs recommended]
- **Algorithm**: [Current vs recommended]

## Caching Recommendations
1. [Cache opportunity 1]
2. [Cache opportunity 2]

## Scalability Assessment
- **Current Capacity**: [Estimated concurrent users]
- **Bottlenecks at Scale**: [Issues that will arise]
- **Horizontal Scaling Readiness**: [Yes/No/Partial]
- **Recommendations**: [Scaling strategy]

## Performance Metrics
- **Average Page Load Time**: [Estimate]
- **Dashboard Load Time**: [Estimate]
- **Upload Processing Time**: [Estimate]
- **Document Generation Time**: [Estimate]

## Quick Wins ⚡
[Easy optimizations with significant impact]

## Long-term Optimizations
[Architectural changes for performance]

## Load Testing Recommendations
[Suggested load testing scenarios]

## Monitoring Recommendations
[Metrics to track in production]
```

## Key Questions to Answer

1. Are there N+1 query problems?
2. Is image processing optimized?
3. Are database indexes missing?
4. Can caching improve performance?
5. Are file operations efficient?
6. Is memory usage reasonable?
7. Can operations be made async?
8. Are there pagination needs?
9. Is the app ready for scale?
10. What are the biggest bottlenecks?

## Performance Benchmarks to Consider

- Page load time <2 seconds
- Database queries <10 per request
- Image processing <5 seconds per upload
- Document generation <10 seconds
- Support 50+ concurrent users
- Memory usage <512MB under normal load

Begin the performance review now.
