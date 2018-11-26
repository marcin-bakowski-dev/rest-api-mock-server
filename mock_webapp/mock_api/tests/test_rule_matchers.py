from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from mock_api.response_rules import (RequestParamExistsMatcher, RequestParamContainsValueMatcher,
                                     RequestParamNotContainsValueMatcher)


# noinspection PyCallingNonCallable
class AbstractRequestParamMatcher(TestCase):
    factory = APIRequestFactory()
    matcher_cls = None

    def assert_request_param_matcher(self, request_method, request_data, param_name, param_value, expected):
        matcher = self.matcher_cls(param_name, param_value)
        request_method_handler = getattr(self.factory, request_method.lower())
        request = Request(request_method_handler('/api/', data=request_data, format="json"), parsers=[JSONParser()])

        match = matcher.match(request)

        self.assertEqual(match, expected)


class RequestParamExistsMatcherTest(AbstractRequestParamMatcher):
    matcher_cls = RequestParamExistsMatcher

    def test_get_request_param_exists_return_true(self):
        self.assert_request_param_matcher("GET", {"test_param": 123}, "test_param", "test_value", True)

    def test_get_request_param_not_exists_return_false(self):
        self.assert_request_param_matcher("GET", None, "test_param", "test_value", False)

    def test_post_request_param_exists_return_true(self):
        self.assert_request_param_matcher("POST", {"test_param": 123}, "test_param", "test_value", True)

    def test_post_request_param_not_exists_return_false(self):
        self.assert_request_param_matcher("POST", None, "test_param", "test_value", False)


class RequestParamContainsValueMatcherTest(AbstractRequestParamMatcher):
    matcher_cls = RequestParamContainsValueMatcher

    def test_get_request_param_contains_value_return_true(self):
        self.assert_request_param_matcher("GET", {"test_param": "test_value123"}, "test_param", "test_value", True)

    def test_get_request_param_contains_value_return_false(self):
        self.assert_request_param_matcher("GET", {"test_param": "123"}, "test_param", "test_value", False)

    def test_get_request_param_contains_value_return_false_when_param_not_present(self):
        self.assert_request_param_matcher("GET", None, "test_param", "test_value", False)

    def test_post_request_param_contains_value_return_true(self):
        self.assert_request_param_matcher("POST", {"test_param": "test_value123"}, "test_param", "test_value", True)

    def test_post_request_param_contains_value_return_false(self):
        self.assert_request_param_matcher("POST", {"test_param": "123"}, "test_param", "test_value", False)


class RequestParamNotContainsValueMatcherTest(AbstractRequestParamMatcher):
    matcher_cls = RequestParamNotContainsValueMatcher

    def test_get_request_param_not_contains_value_return_false(self):
        self.assert_request_param_matcher("GET", {"test_param": "test_value123"}, "test_param", "test_value", False)

    def test_get_request_param_not_contains_value_return_true(self):
        self.assert_request_param_matcher("GET", {"test_param": "123"}, "test_param", "test_value", True)

    def test_post_request_param_not_contains_value_return_false(self):
        self.assert_request_param_matcher("POST", {"test_param": "test_value123"}, "test_param", "test_value", False)

    def test_post_request_param_not_contains_value_return_true(self):
        self.assert_request_param_matcher("POST", {"test_param": "123"}, "test_param", "test_value", True)

    def test_get_request_param_not_contains_value_return_true_when_param_not_present(self):
        self.assert_request_param_matcher("GET", None, "test_param", "test_value", True)
