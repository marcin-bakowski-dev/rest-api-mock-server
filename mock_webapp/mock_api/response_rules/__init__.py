# -*- coding: utf-8 -*-
from mock_api.response_rules.providers import ResponseRuleProvider
from mock_api.response_rules.rule_matchers import RequestParamExistsMatcher, RequestParamContainsValueMatcher, \
    RequestParamNotContainsValueMatcher

response_rules_provider = ResponseRuleProvider()
response_rules_provider.register_matcher_class(RequestParamExistsMatcher)
response_rules_provider.register_matcher_class(RequestParamContainsValueMatcher)
response_rules_provider.register_matcher_class(RequestParamNotContainsValueMatcher)
