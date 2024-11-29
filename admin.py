from django.contrib import admin
from .models import RequestLog

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'path', 'status_code')
    search_fields = ('path', 'method')
    list_filter = ('status_code', 'method', 'timestamp')
    ordering = ('-timestamp',)