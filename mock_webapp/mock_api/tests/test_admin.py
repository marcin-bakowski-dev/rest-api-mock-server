from unittest.mock import patch, ANY

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from mock_api.models import AccessLog


@patch("requests.request")
class AccessLogAdminTest(TestCase):

    fixtures = ("test_api.json", "test_access_logs.json", "test_users.json")
    API_ENDPOINT_URL = '/api/items/'

    def setUp(self):
        self.client.login(username="admin", password="pass")

    def url(self, access_log_pk):
        return reverse("admin:run_api_endpoint_callback", args=(access_log_pk,))

    def get_first_callback(self, access_log):
        return access_log.api_endpoint.callbacks.first()

    def assert_message(self, message_mock, message):
        message_mock.assert_called_once_with(ANY, ANY, message)

    def test_run_api_endpoint_callback_for_missing_access_log_object_returns_404(self, request_mock):
        response = self.client.get(self.url(9999))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(request_mock.call_count, 0)

    @patch("django.contrib.messages.add_message")
    def test_run_api_endpoint_callback_with_one_callback_defined(self, message_mock, request_mock):
        access_log = AccessLog.objects.get(pk=1)
        callback = self.get_first_callback(access_log)

        response = self.client.get(self.url(access_log.pk))

        self.assertEqual(response.status_code, 302)
        request_mock.assert_called_once_with(callback.method, callback.url, params=callback.get_params(),
                                             headers=callback.get_headers(),
                                             timeout=settings.DEFAULT_CALLBACK_REQUEST_TIMEOUT)
        self.assert_message(message_mock, 'Api endpoint {} callbacks were run'.format(access_log.api_endpoint))

    @patch("django.contrib.messages.add_message")
    def test_run_api_endpoint_callback_without_callback_defined(self, message_mock, request_mock):
        access_log = AccessLog.objects.get(pk=2)

        response = self.client.get(self.url(access_log.pk))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(request_mock.call_count, 0)
        self.assert_message(message_mock, 'No callbacks for api endpoint {}'.format(access_log.api_endpoint))

    @patch("django.contrib.messages.add_message")
    def test_run_api_endpoint_callback_without_api_endpoint(self, message_mock, request_mock):
        access_log = AccessLog.objects.get(pk=3)

        response = self.client.get(self.url(access_log.pk))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(request_mock.call_count, 0)
        self.assertEqual(message_mock.call_count, 0)
