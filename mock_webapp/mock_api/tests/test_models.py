# -*- coding: utf-8 -*-
from django.test import TestCase

from mock_api.models import ApiResponse


class ApiResponseTest(TestCase):
    API_ENDPOINT = {
        "name": "test response",
        "status_code": 200,
        "content": '{"test": "123"}',
    }
    fixtures = ('test_api.json',)

    def add_api_response(self, **kwargs):
        api_response_data = {}
        api_response_data.update(self.API_ENDPOINT, **kwargs)
        return ApiResponse.objects.create(**api_response_data)

    def test_non_empty_response_serialize(self):
        api_response = self.add_api_response(content='{"a": "1"}')

        content = api_response.get_content()

        self.assertEqual(len(content), 1)
        self.assertEqual(content["a"], "1")

    def test_empty_response_serialize(self):
        api_response = self.add_api_response(content='')

        content = api_response.get_content()

        self.assertIsNone(content)

    def test_invalid_json_response_serialize(self):
        api_response = self.add_api_response(content='{invalid')

        with self.assertRaises(ValueError):
            api_response.get_content()
