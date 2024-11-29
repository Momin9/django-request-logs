from django.test import TestCase, Client
from django.urls import reverse

from models import RequestLog


class RequestLogsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create some sample request logs for testing
        RequestLog.objects.create(
            method="GET",
            path="/test-path-1/",
            status_code=200,
            duration=120,
        )
        RequestLog.objects.create(
            method="POST",
            path="/test-path-2/",
            status_code=201,
            duration=150,
        )

    def test_request_logs_view(self):
        """
        Test that the request logs view renders correctly with the logs.
        """
        response = self.client.get(reverse('request_logs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request_logs.html')
        self.assertContains(response, '/test-path-1/')
        self.assertContains(response, '/test-path-2/')

    def test_fetch_latest_logs(self):
        """
        Test that the fetch_latest_logs API returns correct data.
        """
        response = self.client.get(reverse('fetch_latest_logs'))
        self.assertEqual(response.status_code, 200)
        logs = response.json().get('logs', [])
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0]['path'], '/test-path-2/')  # Ordered by timestamp
        self.assertEqual(logs[1]['path'], '/test-path-1/')

    def test_request_log_detail_view(self):
        """
        Test that the request_log_detail_view displays the correct log details.
        """
        log = RequestLog.objects.first()
        response = self.client.get(reverse('request_log_detail_view', args=[log.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request_log_detail.html')
        self.assertContains(response, log.path)
        self.assertContains(response, log.method)
        self.assertContains(response, log.status_code)
