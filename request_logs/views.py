import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timesince import timesince
from .models import RequestLog

def request_logs_view(request):
    """
    View to render a list of all request logs.
    """
    logs = RequestLog.objects.all().order_by('-timestamp')
    return render(request, 'request_logs.html', {'logs': logs})

def fetch_latest_logs(request):
    """
    API endpoint to fetch the latest request logs in JSON format.
    """
    logs = RequestLog.objects.all().order_by('-timestamp')
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

def request_log_detail_view(request, log_id):
    """
    View to display details of a specific request log.
    """
    log = get_object_or_404(RequestLog, id=log_id)
    tags = log.tags.split(",") if log.tags else []

    # Parse JSON fields safely
    def safe_json_parse(data):
        try:
            return json.dumps(json.loads(data), indent=4) if data else "{}"
        except (json.JSONDecodeError, TypeError, ValueError):
            return "{}"

    payload_json = safe_json_parse(log.body)
    headers_json = safe_json_parse(log.headers)
    response_json = safe_json_parse(log.response)

    return render(request, 'request_log_detail.html', {
        'log': log,
        'tags': tags,
        'payload_json': payload_json,
        'headers_json': headers_json,
        'response_json': response_json,
    })
