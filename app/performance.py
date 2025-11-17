"""Performance monitoring middleware for Flask application.

This module provides request timing, database query counting, and logging
to help identify performance bottlenecks in the application.
"""

import time
import logging
from flask import g, request
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Configure logging
logger = logging.getLogger('performance')
logger.setLevel(logging.INFO)


# Track database query count per request
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Track database queries before execution."""
    conn.info.setdefault('query_start_time', []).append(time.time())
    if hasattr(g, 'query_count'):
        g.query_count += 1
    else:
        g.query_count = 1


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Track database queries after execution."""
    total_time = time.time() - conn.info['query_start_time'].pop(-1)
    if hasattr(g, 'total_query_time'):
        g.total_query_time += total_time
    else:
        g.total_query_time = total_time


def init_performance_monitoring(app):
    """Initialize performance monitoring for the Flask app."""

    @app.before_request
    def before_request():
        """Track request start time and initialize query counters."""
        g.start_time = time.time()
        g.query_count = 0
        g.total_query_time = 0.0

    @app.after_request
    def after_request(response):
        """Log performance metrics after each request."""
        if hasattr(g, 'start_time'):
            elapsed_time = time.time() - g.start_time
            query_count = getattr(g, 'query_count', 0)
            total_query_time = getattr(g, 'total_query_time', 0.0)

            # Only log slow requests (> 500ms) or requests with many queries
            if elapsed_time > 0.5 or query_count > 10:
                logger.warning(
                    f"SLOW REQUEST: {request.method} {request.path} | "
                    f"Total: {elapsed_time:.3f}s | "
                    f"Queries: {query_count} ({total_query_time:.3f}s) | "
                    f"Status: {response.status_code}"
                )
            else:
                logger.info(
                    f"{request.method} {request.path} | "
                    f"Time: {elapsed_time:.3f}s | "
                    f"Queries: {query_count} | "
                    f"Status: {response.status_code}"
                )

            # Add performance headers for debugging (only in development)
            if app.debug:
                response.headers['X-Request-Time'] = f'{elapsed_time:.3f}s'
                response.headers['X-Query-Count'] = str(query_count)
                response.headers['X-Query-Time'] = f'{total_query_time:.3f}s'

        return response

    # Configure logging handler if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)

    logger.info("Performance monitoring initialized")
