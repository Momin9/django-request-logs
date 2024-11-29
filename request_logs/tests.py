from django.test import TestCase, Client
from django.urls import reverse

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_path_logging(self):
        """
        Test that a valid path is logged correctly.
        """
        response = self.client.get(reverse('fetch_latest_logs'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_path_logging(self):
        """
        Test that an invalid path is handled gracefully.
        """
        response = self.client.get('/invalid-path/')
        self.assertEqual(response.status_code, 404)

    def test_request_logging_duration(self):
        """
        Ensure middleware calculates request duration without errors.
        """
        with self.assertLogs('django.request', level='INFO') as log:
            self.client.get(reverse('fetch_latest_logs'))
            self.assertTrue(any('Duration' in message for message in log.output))
