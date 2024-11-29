from django.db import models
from django.utils import timezone

class RequestLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=10)
    controller_action = models.CharField(max_length=255, blank=True, null=True)
    middleware = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=500)
    status_code = models.IntegerField()
    duration = models.CharField(max_length=255, blank=True, null=True)  # Duration in milliseconds
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    memory_usage = models.CharField(max_length=50, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    headers = models.TextField()
    body = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    cache_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code} at {self.timestamp}"
