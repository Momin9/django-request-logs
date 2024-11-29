import ast
import json
import logging
import re
import time
import tracemalloc

from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.urls import resolve, Resolver404
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .models import RequestLog

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log incoming requests and their details into the database.
    Excludes specific paths and ensures only relevant requests are logged.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [
            '/request-logs/*',
            '/',
            '/request-logs/',
            '/fetch-latest-logs/',
        ]
        self.excluded_prefixes = [
            '/fetch-latest-logs/',
        ]
        self.excluded_regex_patterns = [
            r'^/request-logs/\d+/$',
        ]

    def is_valid_path(self, path):
        """Check if the path is valid and not explicitly excluded."""
        try:
            resolve(path)
            return path not in self.excluded_paths
        except Resolver404:
            return False

    def should_log_request(self, request):
        """Determine if the request should be logged based on exclusions."""
        if request.path in self.excluded_paths:
            return False
        if any(request.path.startswith(prefix) for prefix in self.excluded_prefixes):
            return False
        if any(re.match(pattern, request.path) for pattern in self.excluded_regex_patterns):
            return False
        return self.is_valid_path(request.path)

    def __call__(self, request):
        if not self.should_log_request(request):
            return self.get_response(request)

        # Start timing and memory tracking
        request.start_time = time.time()
        tracemalloc.start()
        request_body = request.body.decode('utf-8', errors='ignore') if request.body else None

        # Process the request and log the response
        response = self.get_response(request)
        self.process_response(request, response, request_body)
        return response

    def process_response(self, request, response, request_body):
        """Log the request details into the database."""
        if not self.should_log_request(request):
            return response

        duration = int((time.time() - request.start_time) * 1000)
        current, peak = tracemalloc.get_traced_memory()
        memory_usage = f"{peak / 1024 / 1024:.2f} MB"
        tracemalloc.stop()

        cache_key = f"request_cache:{request.path}"
        cache_data = "hit" if cache.get(cache_key) else "missed"
        if cache_data == "missed":
            cache.set(cache_key, response.content, timeout=60)

        try:
            body_dict = json.loads(request_body) if request_body else {}
        except json.JSONDecodeError:
            body_dict = {}

        combined_data = {**body_dict, **request.POST.dict()}

        # Save request details in the database
        RequestLog.objects.create(
            timestamp=timezone.now(),
            hostname=request.get_host(),
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration=duration,
            ip_address=ast.literal_eval(json.dumps(dict(request.headers)))["X-Real-Ip"],
            memory_usage=memory_usage,
            tags=f"{request.path}:{response.status_code}",
            headers=json.dumps(dict(request.headers)),
            body=json.dumps(combined_data),
            response=response.content.decode('utf-8', errors='ignore') if response.content else '',
            cache_data=cache_data,
        )
        return response


class BlockInvalidPathsMiddleware:
    """
    Middleware to block all paths that are not part of the Django application.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [
            '/static/', '/admin/', '/favicon.ico', '/media/',
        ]

    def __call__(self, request):
        if any(request.path.startswith(excluded_path) for excluded_path in self.excluded_paths):
            return self.get_response(request)

        try:
            resolve(request.path)
        except Resolver404:
            logger.warning(f"Blocked invalid path: {request.path}")
            return HttpResponseForbidden("Access Denied: Invalid Path")

        return self.get_response(request)
