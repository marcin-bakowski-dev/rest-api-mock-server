# -*- coding: utf-8 -*-
from django.test import TestCase

from mock_api.response_rules import ResponseRuleProvider, RequestParamMatcher
from mock_api.response_rules.errors import MatchingResponseRuleNotFound, InvalidResponseRuleMatcher


class ResponseRuleProviderTest(TestCase):
    fixtures = ('test_api.json',)

    def setUp(self):
        self.provider = ResponseRuleProvider()

    def assert_allowed_matchers_rules_choices(self, choices, expected_choices):
        self.assertEqual(len(choices), len(expected_choices))
        for choice1, choice2 in zip(sorted(choices), sorted(expected_choices)):
            self.assertEqual(choice1, choice2)

    def test_register_matcher_class(self):
        rules = RequestParamMatcher.get_rules()
        self.provider.register_matcher_class(RequestParamMatcher)

        self.assert_allowed_matchers_rules_choices(self.provider.allowed_matchers_rules_choices(),
                                                   list((i, i) for i in rules))
        for rule in rules:
            self.assertIsNotNone(self.provider.get_matcher(rule, "", ""))
        with self.assertRaises(MatchingResponseRuleNotFound):
            self.provider.get_matcher("INVALID", "", "")

    def test_raises_exception_when_invalid_class_is_registered(self):
        class Invalid(object):
            pass

        with self.assertRaises(InvalidResponseRuleMatcher):
            self.provider.register_matcher_class(Invalid)
