from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from unittest.mock import Mock

from django_requests_loger.middleware import RequestLoggingMiddleware, BlockInvalidPathsMiddleware


class RequestLoggingMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestLoggingMiddleware(Mock(return_value=HttpResponse()))

    def test_should_log_valid_path(self):
        """
        Test that a valid path is logged.
        """
        request = self.factory.get('/valid-path/')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_should_not_log_excluded_path(self):
        """
        Test that excluded paths are not logged.
        """
        request = self.factory.get('/django_requests_loger/')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_should_handle_invalid_path(self):
        """
        Test that invalid paths are handled without breaking.
        """
        request = self.factory.get('/invalid-path/')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

class BlockInvalidPathsMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = BlockInvalidPathsMiddleware(Mock(return_value=HttpResponse()))

    def test_allow_excluded_path(self):
        """
        Test that excluded paths are allowed.
        """
        request = self.factory.get('/static/example.css')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_block_invalid_path(self):
        """
        Test that invalid paths are blocked with a 403 response.
        """
        request = self.factory.get('/unknown-path/')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access Denied: Invalid Path")
