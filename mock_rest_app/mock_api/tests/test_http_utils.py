import json
from unittest.mock import patch

from django.conf import settings

from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from mock_api.http_utils import get_request_headers, get_response_headers, get_user_agent, get_query_string, \
    log_request_and_response, make_request


class HttpUtilsTest(TestCase):

    factory = APIRequestFactory()

    def test_get_request_headers_returns_accept_and_content_headers(self):
        content_type_json = "application/json"
        data = {'title': 'test'}
        request = self.factory.post('/api/', data, content_type=content_type_json, HTTP_ACCEPT=content_type_json)

        headers = get_request_headers(request)

        self.assertEqual(headers["HTTP_ACCEPT"], content_type_json)
        self.assertEqual(headers["CONTENT_TYPE"], content_type_json)
        self.assertEqual(headers["CONTENT_LENGTH"], len(json.dumps(data)))
        self.assertEqual(headers["REMOTE_ADDR"], "127.0.0.1")

    def test_response_headers(self):
        response = Response(status=200, headers={"X-TEST": "TEST"})

        headers = get_response_headers(response)

        self.assertEqual(headers["Status code"], 200)
        self.assertEqual(headers["X-TEST"], "TEST")

    def test_request_user_agent_empty(self):
        request = self.factory.get("/api/")

        user_agent = get_user_agent(request)

        self.assertEqual(user_agent, "")

    def test_request_user_agent_non_empty(self):
        http_user_agent = "DJANGO TEST CLIENT"
        request = self.factory.get("/api/", HTTP_USER_AGENT=http_user_agent)

        user_agent = get_user_agent(request)

        self.assertEqual(user_agent, http_user_agent)

    def test_request_query_string_empty(self):
        request = self.factory.get("/api/")

        query_string = get_query_string(request)

        self.assertEqual(query_string, "")

    def test_request_query_string_non_empty(self):
        request_query_string = "test=123"
        request = self.factory.get("/api/?{}".format(request_query_string))

        query_string = get_query_string(request)

        self.assertEqual(query_string, request_query_string)

    def test_access_log_request_response(self):
        http_user_agent = "DJANGO TEST CLIENT"
        request = Request(self.factory.post('/api/?test_qs', data={"ABC": "ABC"}, format="json",
                                            HTTP_USER_AGENT=http_user_agent),
                          parsers=[JSONParser()])
        response = Response(status=200, data={"status": "API_LOG_OK"}, headers={"X-TEST": "Test"})

        access_log = log_request_and_response(request, response)

        self.assertIsNotNone(access_log.request_time)
        self.assertEqual(access_log.user_agent, http_user_agent)
        self.assertEqual(access_log.path, request.path_info)
        self.assertEqual(access_log.request_method, "POST")
        self.assertEqual(access_log.request_query_string, "test_qs")
        self.assertIn(http_user_agent, access_log.request_headers)
        self.assertIn("ABC", access_log.request_data)
        self.assertEqual(access_log.response_status_code, response.status_code)
        self.assertIn("API_LOG_OK", access_log.response_content)
        self.assertIn("X-TEST", access_log.response_headers)

    @patch("requests.request")
    def test_make_api_callback_request(self, mocked_method):
        url = "http://www.google.com"
        method = "GET"
        params = '{"q": "test"}'
        headers = '{"X-TEST": "TEST"}'

        make_request(method=method, url=url, params=params, headers=headers,
                     timeout=settings.DEFAULT_CALLBACK_REQUEST_TIMEOUT)

        mocked_method.assert_called_once_with(method, url, params=params, headers=headers,
                                              timeout=settings.DEFAULT_CALLBACK_REQUEST_TIMEOUT)
