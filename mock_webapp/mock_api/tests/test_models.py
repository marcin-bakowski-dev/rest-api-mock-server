# -*- coding: utf-8 -*-
from django.test import TestCase

from mock_api.models import ApiEndpoint


class ApiEndpointModelTest(TestCase):
    API_ENDPOINT = {
        "path": "/api/test/",
        "status_code": 200,
        "method": "GET",
        "response": '{"test": "rest"}'
    }

    def add_api_endpoint(self, **kwargs):
        api_endpoint_data = {}
        api_endpoint_data.update(self.API_ENDPOINT, **kwargs)
        return ApiEndpoint.objects.create(**api_endpoint_data)

    def test_non_empty_response_serialize(self):
        api_endpoint = self.add_api_endpoint(response='{"a": "1"}')

        response = api_endpoint.get_response()

        self.assertEqual(len(response), 1)
        self.assertEqual(response["a"], "1")

    def test_empty_response_serialize(self):
        api_endpoint = self.add_api_endpoint(response='')

        response = api_endpoint.get_response()

        self.assertIsNone(response)

    def test_invalid_json_response_serialize(self):
        api_endpoint = self.add_api_endpoint(response='{invalid')

        with self.assertRaises(ValueError):
            api_endpoint.get_response()
