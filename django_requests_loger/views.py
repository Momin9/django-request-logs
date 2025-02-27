import json
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.timesince import timesince

from .models import RequestLog

# Fetch dynamic config with sensible defaults
LOGER_CONFIG = getattr(settings, "DJANGO_REQUESTS_LOGER_CONFIG", {})
SECTION_MAP = LOGER_CONFIG.get("SECTION_MAP", {})
SESSION_TIMEOUT_HOURS = LOGER_CONFIG.get("SESSION_TIMEOUT_HOURS", 12)
DEFAULT_LOG_OFFSET = LOGER_CONFIG.get("DEFAULT_LOG_OFFSET", 0)
DEFAULT_LOG_LIMIT = LOGER_CONFIG.get("DEFAULT_LOG_LIMIT", 100)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Retrieve the user with the given email
            user_instance = User.objects.get(email=email)
            username = user_instance.username  # Get the username for authentication

            # Authenticate using the username and password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('request_logs')  # Redirect to the main page after login
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dynamic_view(request, section):
    """
    Dynamically display pages based on 'section' using a configurable SECTION_MAP.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    # Use the dynamic SECTION_MAP from settings
    if section not in SECTION_MAP:
        return redirect('login')  # or a 404 if you prefer

    title = SECTION_MAP.get(section, 'Unknown')
    return render(request, 'dynamic.html', {'title': title})


@login_required(login_url='login')
def request_logs_view(request):
    """
    Renders the main request logs page.
    Uses a dynamic session timeout from settings.
    """
    if 'session_created' in request.session:
        session_created = request.session['session_created']
        session_creation_time = timezone.datetime.fromtimestamp(session_created, tz=timezone.utc)
        now = timezone.now()
        if now - session_creation_time > timedelta(hours=SESSION_TIMEOUT_HOURS):
            logout(request)
            return JsonResponse({'error': 'Session expired'}, status=403)

    # Set session expiry to SESSION_TIMEOUT_HOURS
    request.session.set_expiry(SESSION_TIMEOUT_HOURS * 3600)

    if 'session_created' not in request.session:
        request.session['session_created'] = timezone.now().timestamp()

    return render(request, 'request_logs.html')


@login_required(login_url='login')
def get_logs(request):
    """
    Returns paginated logs as JSON.
    Pagination offset/limit can be set dynamically via settings.
    """
    offset = int(request.GET.get('offset', DEFAULT_LOG_OFFSET))
    limit = int(request.GET.get('limit', DEFAULT_LOG_LIMIT))

    logs = RequestLog.objects.all().order_by('-timestamp')[offset:offset + limit]
    log_data = [
        {
            'id': log.id,
            'ID': log.controller_action,
            'method': log.method,
            'path': log.path,
            'status_code': log.status_code,
            'duration': log.duration,
            'timestamp': log.timestamp.isoformat(),
        }
        for log in logs
    ]

    return JsonResponse({'logs': log_data, 'has_more': len(logs) == limit})


@login_required(login_url='login')
def fetch_latest_logs(request):
    """
    Returns all logs in descending order.
    """
    logs = RequestLog.objects.all().order_by('-timestamp')
    for log in logs:
        # If log.timestamp is not a datetime object, ensure it's converted properly
        if isinstance(log.timestamp, str):
            log.timestamp = timezone.make_aware(timezone.datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S"))

    logs_data = [
        {
            'id': log.id,
            'method': log.method,
            'path': log.path,
            'status_code': log.status_code,
            'duration': log.duration,
            'timestamp': log.timestamp,
            'timesince': timesince(log.timestamp),
        }
        for log in logs
    ]
    return JsonResponse({'logs': logs_data})


@login_required(login_url='login')
def request_log_detail_view(request, log_id):
    """
    Shows detailed information for a single log entry.
    """
    if 'session_created' in request.session:
        session_created = request.session['session_created']
        session_creation_time = timezone.datetime.fromtimestamp(session_created, tz=timezone.utc)
        now = timezone.now()
        if now - session_creation_time > timedelta(hours=SESSION_TIMEOUT_HOURS):
            logout(request)
            return redirect('login')

    # Refresh the session expiry
    request.session.set_expiry(SESSION_TIMEOUT_HOURS * 3600)

    if 'session_created' not in request.session:
        request.session['session_created'] = timezone.now().timestamp()

    log = get_object_or_404(RequestLog, id=log_id)
    tags = log.tags.split(",") if log.tags else []
    payload_json = json.dumps(json.loads(log.body), indent=4) if log.body else "{}"
    headers_json = json.dumps(json.loads(log.headers), indent=4) if log.headers else "{}"

    response_json = "{}"
    if log.response:
        try:
            response_json = json.dumps(json.loads(log.response), indent=4)
        except json.JSONDecodeError:
            response_json = json.dumps({"data": log.response}, indent=4)

    return render(request, 'request_log_detail.html', {
        'log': log,
        'tags': tags,
        'payload_json': payload_json,
        'headers_json': headers_json,
        'response_json': response_json
    })
