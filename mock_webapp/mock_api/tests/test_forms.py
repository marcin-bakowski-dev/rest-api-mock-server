# -*- coding: utf-8 -*-
from django.test import TestCase
from mock_api.forms import ApiEndpointForm


class ApiEndpointFormTest(TestCase):
    DATA = {"path": "/api/test",
            "method": "GET",
            "status_code": 200,
            "response": '{"test": "case"}'}

    def data(self, **kwargs):
        form_data = {}
        form_data.update(self.DATA, **kwargs)
        return form_data

    def assert_api_endpoint_form_is_not_valid(self, data, error_field):
        form = ApiEndpointForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(error_field, form.errors)

    def assert_api_endpoint_form_is_valid(self, data):
        form = ApiEndpointForm(data=data)

        self.assertTrue(form.is_valid())

    def test_empty_path(self):
        self.assert_api_endpoint_form_is_not_valid(self.data(path=""), "path")

    def test_empty_method(self):
        self.assert_api_endpoint_form_is_not_valid(self.data(method=""), "method")

    def test_invalid_method(self):
        self.assert_api_endpoint_form_is_not_valid(self.data(method="INVALID"), "method")

    def test_empty_status_code(self):
        self.assert_api_endpoint_form_is_not_valid(self.data(status_code=""), "status_code")

    def test_invalid_status_code(self):
        self.assert_api_endpoint_form_is_not_valid(self.data(status_code="INVALID"), "status_code")

    def test_invalid_response(self):
        self.assert_api_endpoint_form_is_not_valid(self.data(response="{INVALID"), "response")

    def test_valid_form(self):
        self.assert_api_endpoint_form_is_valid(self.data())

    def test_valid_form_with_empty_response(self):
        self.assert_api_endpoint_form_is_valid(self.data())
