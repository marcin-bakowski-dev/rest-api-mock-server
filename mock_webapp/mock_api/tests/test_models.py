# -*- coding: utf-8 -*-
from django.test import TestCase

from mock_api.models import ApiResponse, ApiCallback


class ApiModelMixin(object):
    INSTANCE_DATA = None
    model_cls = None

    def add_model_instance(self, **kwargs):
        instance_data = {}
        instance_data.update(self.INSTANCE_DATA, **kwargs)
        return self.model_cls.objects.create(**instance_data)


class ApiResponseTest(ApiModelMixin, TestCase):

    INSTANCE_DATA = {
        "name": "test response",
        "status_code": 200,
        "content": '{"test": "123"}',
    }
    fixtures = ('test_api.json',)
    model_cls = ApiResponse

    def test_non_empty_response_deserialize(self):
        api_response = self.add_model_instance(content='{"a": "1"}')

        content = api_response.get_content()

        self.assertEqual(len(content), 1)
        self.assertEqual(content["a"], "1")

    def test_empty_response_deserialize(self):
        api_response = self.add_model_instance(content='')

        content = api_response.get_content()

        self.assertIsNone(content)

    def test_invalid_json_response_deserialize(self):
        api_response = self.add_model_instance(content='{invalid')

        with self.assertRaises(ValueError):
            api_response.get_content()


class ApiCallbackTest(ApiModelMixin, TestCase):

    INSTANCE_DATA = {
        "name": "test response",
        "method": "GET",
        "url": "http://test.com",
        "params": '{"test": "123"}',
        "headers": '{"x-test": 123}'
    }
    fixtures = ('test_api.json',)
    model_cls = ApiCallback

    def test_non_empty_params_deserialize(self):
        api_callback = self.add_model_instance(params='{"a": "1"}')

        params = api_callback.get_params()

        self.assertEqual(len(params), 1)
        self.assertEqual(params["a"], "1")

    def test_empty_params_serialize(self):
        api_callback = self.add_model_instance(params='')

        params = api_callback.get_params()

        self.assertIsNone(params)

    def test_invalid_json_params_deserialize(self):
        api_callback = self.add_model_instance(params='{invalid')

        with self.assertRaises(ValueError):
            api_callback.get_params()
