# Agent 5: Performance Engineer

## Branch Information
**Branch Name:** `claude/performance-optimization`
**Estimated Time:** 3-5 hours
**Priority:** HIGH

## Role & Responsibilities
You are the Performance Engineer responsible for optimizing the application's performance, scalability, and resource utilization. Your goal is to ensure the application can handle production scale efficiently.

## Mission Objective
Implement database optimization (indexing, query optimization), add pagination for scalability, implement caching, optimize image processing, and add performance monitoring.

## Current Performance Issues

1. **No Database Indexing** - Queries will slow down as data grows
2. **No Pagination** - Dashboard loads ALL work items (will fail at scale)
3. **N+1 Query Problems** - Loading relationships inefficiently
4. **No Caching** - Repeated queries for same data
5. **Unoptimized Images** - Large uploads slow down pages
6. **No Query Monitoring** - Can't identify slow queries
7. **No Response Time Tracking** - No visibility into performance

## Step-by-Step Tasks

### Phase 1: Database Optimization (1-2 hours)

1. **Add Database Indexes in `app/models.py`:**

   Update models with strategic indexes:
   ```python
   from sqlalchemy import Index

   class WorkItem(db.Model):
       __tablename__ = 'work_items'
       # ... existing fields ...

       # Add indexes for frequently queried fields
       __table_args__ = (
           Index('idx_status', 'status'),
           Index('idx_submitted_at', 'submitted_at'),
           Index('idx_assigned_to', 'assigned_to'),
           Index('idx_item_number', 'item_number'),
           Index('idx_submitter_name', 'submitter_name'),
           # Composite index for common filter combinations
           Index('idx_status_submitted', 'status', 'submitted_at'),
       )

   class Photo(db.Model):
       __tablename__ = 'photos'
       # ... existing fields ...

       __table_args__ = (
           Index('idx_work_item_id', 'work_item_id'),
       )

   class Comment(db.Model):
       __tablename__ = 'comments'
       # ... existing fields ...

       __table_args__ = (
           Index('idx_work_item_id', 'work_item_id'),
           Index('idx_created_at', 'created_at'),
       )

   class StatusHistory(db.Model):
       __tablename__ = 'status_history'
       # ... existing fields ...

       __table_args__ = (
           Index('idx_work_item_id', 'work_item_id'),
           Index('idx_changed_at', 'changed_at'),
       )
   ```

2. **Create migration script `migrate_add_indexes.py`:**
   ```python
   """Add performance indexes to database tables."""
   from app import create_app, db
   from app.models import WorkItem, Photo, Comment, StatusHistory

   def add_indexes():
       app = create_app()
       with app.app_context():
           # Indexes are defined in models, this will ensure they're created
           db.create_all()
           print("Indexes created successfully")

   if __name__ == '__main__':
       add_indexes()
   ```

3. **Optimize N+1 queries with eager loading:**

   Update `app/admin.py` - `dashboard()` route:
   ```python
   from sqlalchemy.orm import joinedload

   @bp.route('/dashboard')
   @admin_required
   def dashboard():
       # OLD (N+1 problem):
       work_items = WorkItem.query.all()

       # NEW (eager load photos to avoid N+1):
       work_items = WorkItem.query.options(
           joinedload(WorkItem.photos),
           joinedload(WorkItem.comments)
       ).all()

       # For filtered queries:
       query = WorkItem.query.options(joinedload(WorkItem.photos))

       if status_filter != 'all':
           query = query.filter_by(status=status_filter)

       # ... rest of filtering logic
   ```

4. **Add query profiling for development:**

   Create `app/profiling.py`:
   ```python
   """Database query profiling utilities."""
   from flask import current_app
   from sqlalchemy import event
   from sqlalchemy.engine import Engine
   import time
   import logging

   logger = logging.getLogger('sqlalchemy.profiler')

   def init_profiling(app):
       """Initialize query profiling for development."""
       if app.config.get('PROFILE_QUERIES', False):
           @event.listens_for(Engine, "before_cursor_execute")
           def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
               conn.info.setdefault('query_start_time', []).append(time.time())

           @event.listens_for(Engine, "after_cursor_execute")
           def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
               total_time = time.time() - conn.info['query_start_time'].pop()
               if total_time > 0.1:  # Log slow queries (>100ms)
                   logger.warning(f"Slow query ({total_time:.3f}s): {statement}")
   ```

   Enable in `config.py`:
   ```python
   # Query profiling (development only)
   PROFILE_QUERIES = FLASK_ENV == 'development'
   ```

### Phase 2: Pagination Implementation (1 hour)

1. **Add pagination to `app/admin.py` - `dashboard()` route:**

   ```python
   @bp.route('/dashboard')
   @admin_required
   def dashboard():
       # Get pagination parameters
       page = request.args.get('page', 1, type=int)
       per_page = request.args.get('per_page', 25, type=int)

       # ... existing filter logic ...

       # Paginate query
       pagination = query.paginate(
           page=page,
           per_page=per_page,
           error_out=False
       )

       work_items = pagination.items

       return render_template('admin_dashboard.html',
                            work_items=work_items,
                            pagination=pagination,
                            status_filter=status_filter,
                            sort_by=sort_by,
                            search_query=search_query,
                            format_datetime=format_datetime)
   ```

2. **Update `app/templates/admin_dashboard.html` with pagination UI:**

   Add before closing the main content div:
   ```html
   <!-- Pagination -->
   {% if pagination.pages > 1 %}
   <nav aria-label="Page navigation" class="mt-4">
       <ul class="pagination justify-content-center">
           <!-- Previous Page -->
           <li class="page-item {% if not pagination.has_prev %}disabled{% endif %}">
               <a class="page-link" href="{{ url_for('admin.dashboard',
                   page=pagination.prev_num,
                   status=status_filter,
                   sort=sort_by,
                   search=search_query) if pagination.has_prev else '#' }}">
                   Previous
               </a>
           </li>

           <!-- Page Numbers -->
           {% for page_num in pagination.iter_pages(left_edge=1, right_edge=1, left_current=2, right_current=2) %}
               {% if page_num %}
                   <li class="page-item {% if page_num == pagination.page %}active{% endif %}">
                       <a class="page-link" href="{{ url_for('admin.dashboard',
                           page=page_num,
                           status=status_filter,
                           sort=sort_by,
                           search=search_query) }}">
                           {{ page_num }}
                       </a>
                   </li>
               {% else %}
                   <li class="page-item disabled"><span class="page-link">...</span></li>
               {% endif %}
           {% endfor %}

           <!-- Next Page -->
           <li class="page-item {% if not pagination.has_next %}disabled{% endif %}">
               <a class="page-link" href="{{ url_for('admin.dashboard',
                   page=pagination.next_num,
                   status=status_filter,
                   sort=sort_by,
                   search=search_query) if pagination.has_next else '#' }}">
                   Next
               </a>
           </li>
       </ul>

       <!-- Results Info -->
       <div class="text-center text-muted mt-2">
           Showing {{ pagination.per_page * (pagination.page - 1) + 1 }}
           to {{ [pagination.per_page * pagination.page, pagination.total] | min }}
           of {{ pagination.total }} work items
       </div>
   </nav>
   {% endif %}
   ```

3. **Add pagination configuration to `config.py`:**
   ```python
   # Pagination
   ITEMS_PER_PAGE = 25
   MAX_ITEMS_PER_PAGE = 100
   ```

### Phase 3: Caching Implementation (1-2 hours)

1. **Install Flask-Caching:**
   ```bash
   pip install Flask-Caching
   ```

2. **Configure caching in `app/__init__.py`:**
   ```python
   from flask_caching import Cache

   cache = Cache()

   def create_app():
       app = Flask(__name__)
       # ... existing config ...

       # Configure cache
       cache_config = {
           'CACHE_TYPE': 'SimpleCache',  # Use Redis in production
           'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
       }

       if app.config['FLASK_ENV'] == 'production':
           # Use Redis in production for shared cache across instances
           cache_config = {
               'CACHE_TYPE': 'RedisCache',
               'CACHE_REDIS_URL': app.config.get('REDIS_URL', 'redis://localhost:6379/0'),
               'CACHE_DEFAULT_TIMEOUT': 300
           }

       cache.init_app(app, config=cache_config)

       return app
   ```

3. **Add caching to expensive operations:**

   In `app/admin.py`:
   ```python
   from app import cache

   @bp.route('/dashboard')
   @admin_required
   @cache.cached(timeout=60, query_string=True)  # Cache for 1 minute
   def dashboard():
       # ... existing code ...

   # Clear cache when work items are modified
   @bp.route('/edit/<int:item_id>', methods=['POST'])
   @admin_required
   def edit_item(item_id):
       # ... existing code ...
       cache.clear()  # Clear all cache
       # Or: cache.delete_memoized(dashboard)  # Clear specific function
       return redirect(url_for('admin.view_item', item_id=item_id))
   ```

4. **Cache photo counts and statistics:**
   ```python
   @cache.memoize(timeout=300)
   def get_dashboard_stats():
       """Get cached dashboard statistics."""
       return {
           'total_items': WorkItem.query.count(),
           'submitted': WorkItem.query.filter_by(status='Submitted').count(),
           'in_review': WorkItem.query.filter(
               WorkItem.status.like('%In Review%')
           ).count(),
           'completed': WorkItem.query.filter_by(status='Completed Review').count(),
       }
   ```

5. **Add Redis configuration to `config.py`:**
   ```python
   # Redis Cache (production)
   REDIS_URL = os.environ.get('REDIS_URL')
   ```

### Phase 4: Image Processing Optimization (1 hour)

1. **Optimize `app/utils.py` - `resize_image()` function:**

   ```python
   from PIL import Image, ImageFile
   import io

   # Allow loading of truncated images
   ImageFile.LOAD_TRUNCATED_IMAGES = True

   def resize_image(image_path: str, max_width: int = 576) -> tuple:
       """
       Optimized image resizing with better compression.
       """
       try:
           # Register HEIF opener if available
           try:
               from pillow_heif import register_heif_opener
               register_heif_opener()
           except ImportError:
               pass

           with Image.open(image_path) as img:
               # Get original format
               original_format = img.format

               # Convert to RGB
               if img.mode in ('RGBA', 'LA', 'P'):
                   background = Image.new('RGB', img.size, (255, 255, 255))
                   if img.mode == 'P':
                       img = img.convert('RGBA')
                   background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                   img = background
               elif img.mode != 'RGB':
                   img = img.convert('RGB')

               # Only resize if needed
               if img.width > max_width:
                   ratio = max_width / img.width
                   new_height = int(img.height * ratio)

                   # Use high-quality LANCZOS resampling
                   img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

               # Determine output format and path
               if image_path.lower().endswith(('.heic', '.heif')):
                   image_path = image_path.rsplit('.', 1)[0] + '.jpg'

               # Save with optimized settings
               save_kwargs = {
                   'format': 'JPEG',
                   'quality': 85,
                   'optimize': True,
                   'progressive': True  # Progressive JPEG for faster loading
               }

               # For small images, use higher quality
               if img.width < 800 and img.height < 800:
                   save_kwargs['quality'] = 90

               img.save(image_path, **save_kwargs)

               return img.width, img.height, image_path

       except Exception as e:
           print(f"Error processing image {image_path}: {e}")
           raise
   ```

2. **Add thumbnail generation for dashboard:**

   Create `app/utils.py` - `create_thumbnail()`:
   ```python
   def create_thumbnail(image_path: str, size: tuple = (300, 300)) -> str:
       """Create a thumbnail version of image for faster loading."""
       try:
           thumbnail_path = image_path.rsplit('.', 1)[0] + '_thumb.jpg'

           with Image.open(image_path) as img:
               # Convert to RGB
               if img.mode != 'RGB':
                   img = img.convert('RGB')

               # Create thumbnail
               img.thumbnail(size, Image.Resampling.LANCZOS)

               # Save optimized thumbnail
               img.save(thumbnail_path, 'JPEG', quality=80, optimize=True)

           return thumbnail_path
       except Exception as e:
           print(f"Error creating thumbnail: {e}")
           return image_path  # Return original on error
   ```

3. **Update Photo model to store thumbnail path:**
   ```python
   class Photo(db.Model):
       # ... existing fields ...
       thumbnail_path = db.Column(db.String(500))  # Path to thumbnail
   ```

4. **Use lazy loading in templates:**

   Update `app/templates/admin_dashboard.html`:
   ```html
   <!-- Use thumbnails and lazy loading -->
   <img src="{{ url_for('admin.serve_upload', filename=photo.thumbnail_path or photo.filename) }}"
        loading="lazy"
        alt="{{ photo.caption }}"
        class="img-thumbnail">
   ```

### Phase 5: Performance Monitoring (1 hour)

1. **Create `app/monitoring.py`:**
   ```python
   """Performance monitoring utilities."""
   import time
   import logging
   from functools import wraps
   from flask import request, g
   from datetime import datetime

   logger = logging.getLogger('performance')

   def init_monitoring(app):
       """Initialize performance monitoring."""

       @app.before_request
       def before_request():
           """Track request start time."""
           g.start_time = time.time()

       @app.after_request
       def after_request(response):
           """Log request duration."""
           if hasattr(g, 'start_time'):
               duration = time.time() - g.start_time

               # Log slow requests (> 1 second)
               if duration > 1.0:
                   logger.warning(
                       f"Slow request: {request.method} {request.path} "
                       f"took {duration:.3f}s"
                   )

               # Add response time header
               response.headers['X-Response-Time'] = f"{duration:.3f}s"

           return response

   def track_performance(func):
       """Decorator to track function performance."""
       @wraps(func)
       def wrapper(*args, **kwargs):
           start = time.time()
           result = func(*args, **kwargs)
           duration = time.time() - start

           if duration > 0.5:  # Log if > 500ms
               logger.warning(f"{func.__name__} took {duration:.3f}s")

           return result
       return wrapper
   ```

2. **Add monitoring to `app/__init__.py`:**
   ```python
   from app.monitoring import init_monitoring

   def create_app():
       app = Flask(__name__)
       # ... existing config ...

       if app.config.get('ENABLE_MONITORING', True):
           init_monitoring(app)

       return app
   ```

3. **Add performance logging configuration:**

   In `config.py`:
   ```python
   # Performance Monitoring
   ENABLE_MONITORING = True
   SLOW_REQUEST_THRESHOLD = 1.0  # seconds
   ```

4. **Create performance dashboard endpoint (optional):**

   In `app/admin.py`:
   ```python
   @bp.route('/performance')
   @admin_required
   def performance_dashboard():
       """Show performance metrics (admin only)."""
       stats = {
           'total_work_items': WorkItem.query.count(),
           'total_photos': Photo.query.count(),
           'total_comments': Comment.query.count(),
           'database_size': get_database_size(),
           'cache_stats': cache.get_dict('stats') if cache else {}
       }
       return render_template('admin_performance.html', stats=stats)

   def get_database_size():
       """Get approximate database size."""
       try:
           result = db.session.execute('SELECT pg_database_size(current_database())')
           size_bytes = result.scalar()
           # Convert to MB
           return round(size_bytes / (1024 * 1024), 2)
       except:
           return "N/A"
   ```

### Phase 6: Query Optimization (30 minutes)

1. **Optimize search query in `app/admin.py`:**

   ```python
   # OLD (slow for large datasets):
   if search_query:
       search_pattern = f'%{search_query}%'
       query = query.filter(
           db.or_(
               WorkItem.item_number.ilike(search_pattern),
               WorkItem.description.ilike(search_pattern),
               # ...
           )
       )

   # NEW (faster with indexes):
   if search_query:
       # Use full-text search if available (PostgreSQL)
       if current_app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql'):
           from sqlalchemy import func
           query = query.filter(
               func.to_tsvector('english', WorkItem.description + ' ' + WorkItem.location)
               .match(search_query)
           )
       else:
           # Fallback to LIKE for SQLite
           search_pattern = f'%{search_query}%'
           query = query.filter(
               db.or_(
                   WorkItem.item_number.ilike(search_pattern),
                   WorkItem.description.ilike(search_pattern)
               )
           )
   ```

2. **Add database connection pooling to `config.py`:**
   ```python
   # SQLAlchemy Connection Pool
   SQLALCHEMY_ENGINE_OPTIONS = {
       'pool_pre_ping': True,
       'pool_recycle': 300,
       'pool_size': 10,          # Number of connections to keep
       'max_overflow': 20,       # Max additional connections
       'pool_timeout': 30        # Timeout for getting connection
   }
   ```

### Phase 7: Asset Optimization (30 minutes)

1. **Add CSS/JS minification in production:**

   Create `app/static/build.py`:
   ```python
   """Build script to minify assets."""
   import os
   import csscompressor
   import jsmin

   def minify_css():
       css_dir = 'app/static/css'
       for filename in os.listdir(css_dir):
           if filename.endswith('.css') and not filename.endswith('.min.css'):
               with open(f'{css_dir}/{filename}', 'r') as f:
                   content = f.read()
               minified = csscompressor.compress(content)
               with open(f'{css_dir}/{filename.replace(".css", ".min.css")}', 'w') as f:
                   f.write(minified)

   def minify_js():
       js_dir = 'app/static/js'
       for filename in os.listdir(js_dir):
           if filename.endswith('.js') and not filename.endswith('.min.js'):
               with open(f'{js_dir}/{filename}', 'r') as f:
                   content = f.read()
               minified = jsmin.jsmin(content)
               with open(f'{js_dir}/{filename.replace(".js", ".min.js")}', 'w') as f:
                   f.write(minified)
   ```

2. **Use minified assets in production:**

   Update `app/templates/base.html`:
   ```html
   {% if config.FLASK_ENV == 'production' %}
       <link rel="stylesheet" href="{{ url_for('static', filename='css/style.min.css') }}">
       <script src="{{ url_for('static', filename='js/main.min.js') }}"></script>
   {% else %}
       <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
       <script src="{{ url_for('static', filename='js/main.js') }}"></script>
   {% endif %}
   ```

## Files You MUST Modify/Create

### Create:
- `migrate_add_indexes.py` - Add database indexes
- `app/profiling.py` - Query profiling utilities
- `app/monitoring.py` - Performance monitoring
- `app/static/build.py` - Asset minification (optional)

### Modify:
- `app/models.py` - Add indexes to tables
- `app/admin.py` - Add pagination, caching, eager loading
- `app/utils.py` - Optimize image processing
- `app/__init__.py` - Initialize cache and monitoring
- `config.py` - Add pagination, cache, monitoring config
- `requirements.txt` - Add Flask-Caching
- `app/templates/admin_dashboard.html` - Add pagination UI

### DO NOT Modify:
- Authentication logic
- Core business logic (unless optimizing queries)
- Templates (except adding pagination)

## Quality Checklist

### Database Optimization:
- [ ] Indexes added to frequently queried fields
- [ ] N+1 queries eliminated with eager loading
- [ ] Query profiling enabled in development
- [ ] Connection pooling configured

### Pagination:
- [ ] Pagination implemented on dashboard
- [ ] Pagination UI functional
- [ ] Filters work with pagination
- [ ] Page size configurable

### Caching:
- [ ] Flask-Caching installed
- [ ] Dashboard responses cached
- [ ] Cache invalidation on updates
- [ ] Redis configured for production (optional)

### Image Optimization:
- [ ] Images resized with high quality
- [ ] Progressive JPEG enabled
- [ ] Thumbnails generated
- [ ] Lazy loading implemented

### Monitoring:
- [ ] Request timing tracked
- [ ] Slow queries logged
- [ ] Response time headers added
- [ ] Performance dashboard created (optional)

### Testing:
- [ ] Pagination tested with large dataset
- [ ] Cache tested (verify hits/misses)
- [ ] Query performance improved (measure before/after)
- [ ] No performance regressions

## Performance Benchmarking

Create `benchmark.py`:
```python
"""Performance benchmarking script."""
import time
import statistics
from app import create_app, db
from app.models import WorkItem

def benchmark_query(description, query_func, iterations=100):
    """Benchmark a database query."""
    print(f"\nBenchmarking: {description}")

    times = []
    for _ in range(iterations):
        start = time.time()
        query_func()
        duration = time.time() - start
        times.append(duration)

    print(f"  Average: {statistics.mean(times):.3f}s")
    print(f"  Median:  {statistics.median(times):.3f}s")
    print(f"  Min:     {min(times):.3f}s")
    print(f"  Max:     {max(times):.3f}s")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Benchmark different queries
        benchmark_query(
            "Load all work items (no eager loading)",
            lambda: WorkItem.query.all()
        )

        benchmark_query(
            "Load all work items (with eager loading)",
            lambda: WorkItem.query.options(joinedload(WorkItem.photos)).all()
        )

        benchmark_query(
            "Paginated query",
            lambda: WorkItem.query.paginate(page=1, per_page=25)
        )
```

## Success Criteria

- ✅ Database indexes added and working
- ✅ Dashboard pagination functional
- ✅ Page load time < 2 seconds (for 1000+ items)
- ✅ Caching reduces database queries by 50%+
- ✅ Image processing optimized (< 2 seconds per image)
- ✅ Slow queries identified and logged
- ✅ No N+1 query problems
- ✅ Performance monitoring active

## Deliverables

1. Database indexes and migrations
2. Pagination on admin dashboard
3. Caching implementation
4. Optimized image processing
5. Performance monitoring system
6. Benchmark results showing improvements
7. Documentation of optimizations

## Resources

- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/20/faq/performance.html)
- [Flask-Caching](https://flask-caching.readthedocs.io/)
- [Pillow Performance](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)
- [Database Indexing Best Practices](https://use-the-index-luke.com/)

## Notes

- Test with realistic data volumes (1000+ work items)
- Measure before and after performance
- Consider adding APM tool (New Relic, DataDog) for production
- Monitor Railway metrics (CPU, memory, response time)
- Consider Redis for production caching

---

**Ready to start?** Begin with Phase 1 (Database Optimization) and measure performance improvements after each phase!
