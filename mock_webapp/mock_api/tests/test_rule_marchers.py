# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from mock_api.response_rules import RequestParamMatcher


class RequestParamMatcherTest(TestCase):
    factory = APIRequestFactory()

    def assert_request_param_matcher(self, request_method, request_data, rule, param_name, param_value, expected):
        matcher = RequestParamMatcher(rule, param_name, param_value)
        request_method_handler = getattr(self.factory, request_method.lower())
        request = Request(request_method_handler('/api/', data=request_data))

        match = matcher.match(request)

        self.assertEqual(match, expected)

    def test_get_request_param_exists_return_true(self):
        self.assert_request_param_matcher("GET", {"test_param": 123}, "PARAM_EXISTS", "test_param", "test_value", True)

    def test_get_request_param_not_exists_return_false(self):
        self.assert_request_param_matcher("GET", None, "PARAM_EXISTS", "test_param", "test_value", False)

    def test_post_request_param_exists_return_true(self):
        self.assert_request_param_matcher("POST", {"test_param": 123}, "PARAM_EXISTS", "test_param", "test_value", True)

    def test_post_request_param_not_exists_return_false(self):
        self.assert_request_param_matcher("POST", None, "PARAM_EXISTS", "test_param", "test_value", False)

    def test_get_request_param_contains_value_return_true(self):
        self.assert_request_param_matcher("GET", {"test_param": "test_value123"}, "PARAM_CONTAINS_VALUE", "test_param",
                                          "test_value", True)

    def test_get_request_param_contains_value_return_false(self):
        self.assert_request_param_matcher("GET", {"test_param": "123"}, "PARAM_CONTAINS_VALUE", "test_param",
                                          "test_value", False)

    def test_post_request_param_contains_value_return_true(self):
        self.assert_request_param_matcher("POST", {"test_param": "test_value123"}, "PARAM_CONTAINS_VALUE", "test_param",
                                          "test_value", True)

    def test_post_request_param_contains_value_return_false(self):
        self.assert_request_param_matcher("POST", {"test_param": "123"}, "PARAM_CONTAINS_VALUE", "test_param",
                                          "test_value", False)

    def test_get_request_param_not_contains_value_return_false(self):
        self.assert_request_param_matcher("GET", {"test_param": "test_value123"}, "PARAM_NOT_CONTAINS_VALUE",
                                          "test_param", "test_value", False)

    def test_get_request_param_not_contains_value_return_true(self):
        self.assert_request_param_matcher("GET", {"test_param": "123"}, "PARAM_NOT_CONTAINS_VALUE", "test_param",
                                          "test_value", True)

    def test_post_request_param_not_contains_value_return_false(self):
        self.assert_request_param_matcher("POST", {"test_param": "test_value123"}, "PARAM_NOT_CONTAINS_VALUE",
                                          "test_param", "test_value", False)

    def test_post_request_param_not_contains_value_return_true(self):
        self.assert_request_param_matcher("POST", {"test_param": "123"}, "PARAM_NOT_CONTAINS_VALUE", "test_param",
                                          "test_value", True)
