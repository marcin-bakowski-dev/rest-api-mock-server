# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch

from mock_api.models import ApiEndpoint


class MockApiViewTest(APITestCase):
    fixtures = ('test_apiendpoints.json',)
    PATH = '/api/items/'

    def test_undefined_path(self):
        response = self.client.get("/undefined/")

        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def get_api_endpoint(self, path, method):
        return ApiEndpoint.objects.get(path=path, method=method)

    def assert_api_endpoint_response(self, path, method, **kwargs):
        api_endpoint = self.get_api_endpoint(path, method)
        method_handler = lambda request_method: getattr(self.client, request_method.lower())

        response = method_handler(method)(self.PATH, **kwargs)

        self.assertEqual(response.status_code, api_endpoint.status_code)
        self.assertEqual(response.content.decode(encoding="UTF-8"), api_endpoint.response)

    def test_get_request(self):
        self.assert_api_endpoint_response(self.PATH, "GET")

    def test_post_request(self):
        self.assert_api_endpoint_response(self.PATH, "POST", data={"test": "data"})

    def test_put_request(self):
        self.assert_api_endpoint_response(self.PATH, "PUT", data={"test": "data"})

    def test_patch_request(self):
        self.assert_api_endpoint_response(self.PATH, "PATCH", data={"test": "data"})

    def test_delete_request(self):
        self.assert_api_endpoint_response(self.PATH, "DELETE")

    def test_options_request(self):
        self.assert_api_endpoint_response(self.PATH, "OPTIONS")

    @patch("mock_api.http_utils.log_request_and_response")
    def test_access_log_request_response(self, mock_method):
        http_user_agent = "TEST DJANGO CLIENT"

        self.client.get(self.PATH, HTTP_USER_AGENT=http_user_agent)

        self.assertEqual(mock_method.call_count, 1)
