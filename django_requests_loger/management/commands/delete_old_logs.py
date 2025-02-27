from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from django_requests_loger.models import RequestLog


class Command(BaseCommand):
    help = 'Delete RequestLog entries older than one week'

    def handle(self, *args, **kwargs):
        one_week_ago = timezone.now() - timedelta(weeks=1)
        deleted_logs_count, _ = RequestLog.objects.filter(timestamp__lt=one_week_ago).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_logs_count} old RequestLog entries'))
